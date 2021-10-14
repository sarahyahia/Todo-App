from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from utils.setup_tests import TestSetup



class TestViews(TestSetup):
    
    def test_should_show_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/register.html')
        
    def test_should_show_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')
        
    def test_should_signup_user(self):        
        response = self.client.post(reverse('register'),self.user)
        self.assertEqual(response.status_code, 302)
        
        
    def test_should_not_signup_user_with_taken_username(self):
        
        self.client.post(reverse('register'),self.user)
        response = self.client.post(reverse('register'),self.user)
        self.assertEqual(response.status_code, 409)
        storage = get_messages(response.wsgi_request)
        self.assertIn('Username is taken, choose another one',list(map(lambda x : x.message, storage)))
        
        
    def test_should_not_signup_user_with_taken_email(self):
        
        self.test_user2 = {
            'username': 'username2',
            'email' : self.user.get('email'),
            'password' : 'password',
            'password2' : 'password'
        }
        self.client.post(reverse('register'),self.user)
        response = self.client.post(reverse('register'),self.test_user2)
        self.assertEqual(response.status_code, 409)
        
        
    def test_should_login_successfully(self):
        user = self.create_test_user()
        response = self.client.post(reverse('login'), {
            'username': user.username,
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        storage = get_messages(response.wsgi_request)
        self.assertIn(f'Welcome {user.username}',list(map(lambda x : x.message, storage)))
        
    def test_should_not_login_wrong_password(self):
        user = self.create_test_user()
        response = self.client.post(reverse('login'), {
            'username': user.username,
            'password': 'password12'
        })
        self.assertEqual(response.status_code, 401)
        storage = get_messages(response.wsgi_request)
        self.assertIn('wrong user or password',list(map(lambda x : x.message, storage)))
        
    def test_should_not_login_not_verified(self):
        user = self.create_test_user_two()
        response = self.client.post(reverse('login'), {
            'username': user.username,
            'password': 'password12!'
        })
        self.assertEqual(response.status_code, 401)
        storage = get_messages(response.wsgi_request)
        self.assertIn('Email is not verified, please check your email inbox',list(map(lambda x : x.message, storage)))
        