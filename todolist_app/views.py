from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import (
    CreateView,
    DeleteView,
    UpdateView,
)
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from pure_pagination.mixins import PaginationMixin
from django.views.generic import TemplateView
from .models import Todo, TaskStatus


num_pagination = 3


class TodoListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = Todo
    task_status = TaskStatus
    paginate_by = num_pagination

    def get_queryset(self):
        my_task_status = self.task_status.objects.get(name='Done')
        return self.model.objects.filter(
            assigned_user=self.request.user
        ).exclude(done=my_task_status)


class TodoDoneListView(LoginRequiredMixin, PaginationMixin, TemplateView):
    template_name = "todolist_app/todo_done_task.html"
    model = Todo
    task_status = TaskStatus
    paginate_by = num_pagination

    def get_context_data(self, **kwargs):
        my_task_status = self.task_status.objects.get(name='Done')
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.model.objects.filter(done=my_task_status)
        return context

    def get_object(self):
        obj = super().get_object().assigned_user.id
        if obj != self.request.user.id:
            raise PermissionDenied
        else:
            return super().get_object()


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ['title', 'description', 'assigned_user', 'done', 'priority']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse('todo_detail', args=(self.object.id,))
    success_url = reverse_lazy('todo_list')


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ['title', 'description', 'done', 'priority']
    success_url = reverse_lazy('todo_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def get_object(self):
        obj = super().get_object().assigned_user.id
        if obj != self.request.user.id:
            raise PermissionDenied
        else:
            return super().get_object()


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    fields = ['title', 'description', 'assigned_user', 'done', 'priority']
    success_url = reverse_lazy('todo_list')

    def get_object(self):
        obj = super().get_object().assigned_user.id
        if obj != self.request.user.id:
            raise PermissionDenied
        else:
            return super().get_object()


class TodoReasignView(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ['assigned_user']
    success_url = reverse_lazy('todo_list')

    def get_object(self):
        obj = super().get_object().assigned_user.id
        if obj != self.request.user.id:
            raise PermissionDenied
        else:
            return super().get_object()


class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo

    def get_object(self):
        obj = super().get_object().assigned_user.id
        if obj != self.request.user.id:
            raise PermissionDenied
        else:
            return super().get_object()
