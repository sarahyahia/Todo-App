from django.test import TestCase
from authentication.models import User
from todo.models import Todo
from faker import Faker
from django.urls import reverse


class TestSetup(TestCase):

    def setUp(self):
        
        self.faker = Faker()
        self.password = self.faker.paragraph(nb_sentences=5)
        self.user = {
            'username': self.faker.name().replace(' ', ''),
            'email' : self.faker.email(),
            'password' : self.password,
            'password2' : self.password
        }
        
        
    def create_test_user(self):
        user = User.objects.create_user(
            username='username',
            email='email@hmaile3.com',
            is_email_verified='True'
        )
        user.set_password('password123')
        user.save()
        return user


    def create_test_user_two(self):
        user = User.objects.create_user(
            username='username2', email='email2@app.com')
        user.set_password('password12!')
        user.save()
        return user
    
    
    def create_test_task(self):
        user = self.create_test_user()
        
        self.client.post(reverse("login"), {
            'username': user.username,
            'password': 'password123'
        })
        task = Todo.objects.create(
            title= 'title',
            description= 'description',
            owner = user
        )
        return task
    
    def tearDown(self):
        return super().tearDown()
