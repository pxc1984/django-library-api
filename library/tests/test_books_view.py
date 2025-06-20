from django.urls import reverse
from rest_framework import status

from library.models import Book
from library.tests.base import UserBookAPITest


class BooksViewTestSet(UserBookAPITest):
    def test_forbidden_method(self):
        url = reverse('books view')

        new_book_data = {
            'title': 'New Book',
            'author': 'New Author',
            'isbn': '9876543210123',
            'available_copies': 3
        }

        response = self.client.put(url, new_book_data)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

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
