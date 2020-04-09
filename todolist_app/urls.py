from django.urls import path
from .views import (
    TodoListView,
    TodoCreateView,
    TodoDeleteView,
    TodoUpdateView,
    TodoReasignView,
    TodoDetailView,
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', TodoListView.as_view(), name='todo_list'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('create/', TodoCreateView.as_view(), name='todo_create'),
    path('update/<pk>', TodoUpdateView.as_view(), name='todo_update'),
    path('delete/<pk>', TodoDeleteView.as_view(), name='todo_delete'),
    path('reasign/<pk>', TodoReasignView.as_view(), name='todo_reasign'),
    path('detail/<pk>', TodoDetailView.as_view(), name='todo_detail'),
]
