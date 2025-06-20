from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class BaseTestCase(APITestCase):
    def setUp(self):
        self.test_user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com'
        }


class RegisterAPITest(BaseTestCase):
    def test_successful_registration(self):
        url = reverse('register')
        response = self.client.post(url, self.test_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_invalid_registration(self):
        url = reverse('register')
        invalid_data = {
            'username': 'testuser',
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bad_password_registration(self):
        url = reverse('register')
        invalid_data = {
            "username": "testuser",
            "password": "weak",
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class PingAPITest(BaseTestCase):
    def test_ping_endpoint(self):
        url = reverse('ping')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'pong'})
