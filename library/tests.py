from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from library.models import Book


class BaseTestCase(APITestCase):
    def setUp(self):
        # Create normal user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
        )

        # Create admin user
        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin123',
            email='admin@example.com',
            is_staff=True
        )

        self.sample_book = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'available_copies': 5
        }
        self.book = Book.objects.create(**self.sample_book)

    def authenticate_user(self):
        """
        Helper function that authenticates as a normal user.
        :return:
        """
        self.client.force_authenticate(user=self.user)

    def authenticate_admin(self):
        """
        Helper function that authenticates as an admin user.
        :return:
        """
        self.client.force_authenticate(user=self.admin_user)


class BookAPITest(BaseTestCase):
    def test_list_books_empty(self):
        # Delete the book created in setUp
        Book.objects.all().delete()
        
        url = reverse('books view')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'books': []})

    def test_list_books_with_data(self):
        url = reverse('books view')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['books']), 1)
        self.assertIn(str(self.book), response.data['books'])

    def test_add_new_book_success(self):
        self.authenticate_admin()
        response, new_book_data = self._add_new_book()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'ok'})
        self.assertTrue(Book.objects.filter(isbn=new_book_data['isbn']).exists())

    def test_add_new_book_wrong_permissions(self):
        self.authenticate_user()
        response, new_book_data = self._add_new_book()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Book.objects.filter(isbn=new_book_data['isbn']).exists())

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

    def test_add_existing_book_increases_copies(self):
        self.authenticate_admin()
        url = reverse('books view')

        additional_copies = {
            'title': self.sample_book['title'],
            'author': self.sample_book['author'],
            'isbn': self.sample_book['isbn'],
            'available_copies': 3
        }
        
        initial_copies = self.book.available_copies
        response = self.client.post(url, additional_copies)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, initial_copies + additional_copies['available_copies'])

    def test_add_book_missing_title(self):
        self.authenticate_admin()
        url = reverse('books view')

        invalid_book = {
            'author': 'Test Author',
            'isbn': '1234567890123',
            'available_copies': 5
        }
        
        response = self.client.post(url, invalid_book)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'message': 'Please provide book title'})

    def test_add_book_missing_author(self):
        self.authenticate_admin()
        url = reverse('books view')

        invalid_book = {
            'title': 'Test Book',
            'isbn': '1234567890123',
            'available_copies': 5
        }
        
        response = self.client.post(url, invalid_book)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'message': 'Please provide book author'})

    def test_add_book_missing_isbn(self):
        self.authenticate_admin()
        url = reverse('books view')

        invalid_book = {
            'title': 'Test Book',
            'author': 'Test Author',
            'available_copies': 5
        }
        
        response = self.client.post(url, invalid_book)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'message': 'Please provide book isbn'})

    def test_add_book_invalid_copies(self):
        self.authenticate_admin()
        url = reverse('books view')

        invalid_book = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'available_copies': 'invalid'
        }
        
        response = self.client.post(url, invalid_book)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)

    def test_add_book_zero_copies(self):
        self.authenticate_admin()
        url = reverse('books view')

        invalid_book = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'available_copies': 0
        }
        
        response = self.client.post(url, invalid_book)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'message': 'Please provide available copies'})

class BorrowAPITest(BaseTestCase):
    ...
