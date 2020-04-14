from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import (
    CreateView,
    DeleteView,
    UpdateView,
)
from django.urls import reverse_lazy
from pure_pagination.mixins import PaginationMixin
from .models import Todo, TaskStatus


num_pagination = 5


class FilterTodoOwner:
    def get_queryset(self):
        return Todo.objects.filter(assigned_user=self.request.user)


class TodoListView(LoginRequiredMixin, FilterTodoOwner, PaginationMixin, ListView):
    model = Todo
    task_status = TaskStatus
    paginate_by = num_pagination
    # done = ???

    def get_queryset(self):
        return self.model.objects.filter(
            assigned_user=self.request.user,
            # done=self.status
        )


class TodoDoneListView(LoginRequiredMixin, FilterTodoOwner, PaginationMixin, ListView):
    template_name = "todolist_app/todo_done_task.html"
    model = Todo
    task_status = TaskStatus
    paginate_by = num_pagination

    def get_queryset(self):
        my_task_status = self.task_status.objects.get(name='Done')
        to_show = self.model.objects.filter(done=my_task_status)
        return to_show


class TodoCreateView(LoginRequiredMixin, FilterTodoOwner, CreateView):
    model = Todo
    fields = ['title', 'description', 'assigned_user', 'done', 'priority']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse('todo_detail', args=(self.object.id,))
    success_url = reverse_lazy('todo_list')


class TodoUpdateView(LoginRequiredMixin, FilterTodoOwner, UpdateView):
    model = Todo
    fields = ['title', 'description', 'done', 'priority']
    success_url = reverse_lazy('todo_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class TodoDeleteView(LoginRequiredMixin, FilterTodoOwner, DeleteView):
    model = Todo
    fields = ['title', 'description', 'assigned_user', 'done', 'priority']
    success_url = reverse_lazy('todo_list')


class TodoReasignView(LoginRequiredMixin, FilterTodoOwner, UpdateView):
    model = Todo
    fields = ['assigned_user']
    success_url = reverse_lazy('todo_list')


class TodoDetailView(LoginRequiredMixin, FilterTodoOwner, DetailView):
    model = Todo
