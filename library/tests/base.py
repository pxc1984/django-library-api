import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from library.models import Book, Borrow


class BookAPITest(APITestCase):
    user: User

    @classmethod
    def setUpTestData(cls):
        # Create a normal user
        cls.normal_user = User.objects.create_user(
            username='testuser',
            password='testpass123',
        )

        # Create admin user
        cls.admin_user = User.objects.create_user(
            username='admin',
            password='admin123',
            email='admin@example.com',
            is_staff=True
        )
        cls.user = cls.normal_user

    def setUp(self):
        self.sample_book = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'available_copies': 5
        }
        self.book = Book.objects.create(**self.sample_book)
        self.authenticate()

    def authenticate(self):
        """
        Helper function that authenticates as a self.user.
        :return:
        """
        self.authenticateAs(self.user)

    def unauthenticate(self):
        self.authenticateAs(None)

    def authenticateAs(self, user: User | None):
        self.client.force_authenticate(user=user)

    def _add_new_book(self):
        url = reverse('books view')

        new_book_data = {
            'title': 'New Book',
            'author': 'New Author',
            'isbn': '9876543210123',
            'available_copies': 3
        }

        response = self.client.post(url, new_book_data)
        return response, new_book_data


class AdminBookAPITest(BookAPITest):
    def setUp(self):
        self.user = self.admin_user
        super().setUp()


class UserBookAPITest(BookAPITest):
    def setUp(self):
        self.user = self.user
        super().setUp()
