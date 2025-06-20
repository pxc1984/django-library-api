import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from library.models import Book, Borrow
from library.tests.base import AdminBookAPITest, UserBookAPITest, BookAPITest


class BookAdditionTestSet(AdminBookAPITest):
    def test_add_new_book_success(self):
        response, new_book_data = self._add_new_book()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'ok'})
        self.assertTrue(Book.objects.filter(isbn=new_book_data['isbn']).exists())

    def test_add_existing_book_increases_copies(self):
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
        url = reverse('books view')

        invalid_book = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'available_copies': 0
        }

        response = self.client.post(url, invalid_book)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserBookAdditionTest(UserBookAPITest):
    def test_add_new_book_wrong_permissions(self):
        response, new_book_data = self._add_new_book()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Book.objects.filter(isbn=new_book_data['isbn']).exists())
