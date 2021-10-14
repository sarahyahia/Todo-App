from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from utils.setup_tests import TestSetup
from todo.models import Todo


class TestViews(TestSetup):
    
    def test_should_create_todo(self):
        user = self.create_test_user()
        
        self.client.post(reverse("login"), {
            'username': user.username,
            'password': 'password123'
        })
        
        todos = Todo.objects.filter(owner=user)
        self.assertEqual(todos.count(), 0)

        task = {
            'title': 'title',
            'description': 'description',
            'owner': user
        }
        
        response = self.client.post(reverse('create_todo'),task)
        
        todos = Todo.objects.filter(owner=user)
        self.assertEqual(todos.count(), 1)
        
        self.assertEqual(response.status_code, 302)
        
        
    def test_should_edit_todo(self):
        
        task = self.create_test_task()
        
        task.title = 'hello'
        context={
            'title': 'hello',
            'description': task.description,
            'owner': task.owner,
        }
        response = self.client.post(reverse('edit', kwargs={'id': task.id}),context)
        todos = Todo.objects.get(id=task.id)
        self.assertEqual(todos.title,'hello')
        
        self.assertEqual(response.status_code, 302)
        
    def test_should_edit_todo(self):
        
        task = self.create_test_task()
        response = self.client.post(reverse('delete', kwargs={'id': task.id}))
        self.assertEqual(response.status_code, 302)
        