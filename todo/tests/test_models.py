from django.test import TestCase
from authentication.models import User
from todo.models import Todo
from utils.setup_tests import TestSetup


class TestModel(TestSetup):
    
    def test_should_create_todo(self):
        user = self.create_test_user()
        
        task = Todo.objects.create(
            title='title',
            description='description',
            is_completed=True,
            owner=user,
        )
        task.save()
        self.assertEqual(str(task),'title') # testing title because it's in __str__ function in Todo Model