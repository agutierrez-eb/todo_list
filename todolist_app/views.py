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
from .models import Todo


class TodoListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = Todo

    paginate_by = 5
    # Replace it for your model or use the queryset attribute instead
    # object = Todo

    def get_queryset(self):
        return self.model.objects.filter(assigned_user=self.request.user)


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
    fields = ['title', 'description', 'done']
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
