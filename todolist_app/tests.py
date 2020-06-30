from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from .models import Priority, TaskStatus, Todo


class TestTodoList(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()

    def test_correct_login(self):
        self.credentials = {
            'username': 'test',
            'password': 'test',
        }
        response = self.client.post('/login', self.credentials)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_incorrect_login(self):
        response = self.client.post('/login', {'username': 'test', 'password': 'incorrect'})
        self.assertEqual(response.status_code, 200)


class CreateTodo(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.priority = Priority.objects.create(name="Urgent", order=3)
        self.done = TaskStatus.objects.create(name="Not started")

    def test_create_todo(self):
        self.client.login(username='test', password='test')
        data = {
            'title': 'create_todo',
            'description': 'description todo',
            'assigned_user': self.user.id,
            'done': self.done.id,
            'priority': self.priority.id,
        }
        response = self.client.post("/create/", data)
        self.assertRedirects(response, "/")
        self.assertEqual(response.status_code, 9999999)
        self.assertEqual(Todo.objects.filter(assigned_user=self.user).count(), 1)

    def test_create_todo_fails(self):
        self.client.login(username='test', password='test')
        data = {
            'title': '',
            'description': 'description todo',
            'assigned_user': self.user.id,
            'done': self.done.id,
            'priority': self.priority.id,
        }
        response = self.client.post("/create/", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Todo.objects.filter(assigned_user=self.user).count(), 0)


class ViewTodo(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.priority = Priority.objects.create(name="Urgent", order=3)
        self.done = TaskStatus.objects.create(name="Not started")
        # import ipdb; ipdb.set_trace()
        self.task = Todo.objects.create(
            title="task1",
            description="description1",
            assigned_user=self.user,
            done=self.done,
            created='2020-04-10',
            updated='2020-04-10',
            created_by=self.user,
            updated_by=self.user,
            priority=self.priority,
        )

    def test_view(self):
        self.assertEqual(Todo.objects.filter(title='task1').count(), 1)











