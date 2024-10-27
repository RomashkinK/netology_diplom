from django.test import TestCase
from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import Product, Order

# Create your tests here.
User = get_user_model()

class RegisterAccountTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_buyer(self):
        url = reverse('backend:user-register')
        data = {
            'first_name': 'Alex',
            'last_name': 'Queen',
            'email': 'alex@example.com',
            'password': 'password123',
            'company': 'Example Company',
            'position': 'Developer'       
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ConfirmAccountTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(first_name='Alan', last_name='Turner', email='Alan@example.com', password='password123456')
    def test_confirm_email(self):
        token = Token.objects.create(user=self.user)
        url = reverse('backend:user-register-confirm')
        data = {
            'email': 'Alan@example.com',
            'token': token.key
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(first_name='Alex', last_name='Queen', email='Alex@example.com', password='password123')
    def test_login(self):
        url = reverse('backend:user-login')
        data = {
            'email': 'Alex@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class AccoutnDetailsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(first_name='Alex', last_name='Reed', email='AlexR@example.com', password='password123')
        self.token = Token.objects.create(user=self.user)
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.force_authenticate(user=self.user)
    def test_get_user_profile(self):
        url = reverse('backend:user-details')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ShopViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(first_name='Alex', last_name='Reed', email='AlexR@example.com', password='password123')
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_get_shops(self):
        url = reverse('backend:shops')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CategoryViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(first_name='Alex', last_name='Reed', email='AlexR@example.com', password='password123')
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_get_categories(self):
        url = reverse('backend:categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
