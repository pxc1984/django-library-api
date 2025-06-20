import datetime

from django.urls import reverse
from rest_framework import status

from library.models import Borrow
from library.tests.base import UserBookAPITest


class ReturnBookViewTestSet(UserBookAPITest):
    def test_return_book_successful(self):
        borrow = Borrow.objects.create(user=self.user, book=self.book)

        url = reverse('return book view')
        response = self.client.post(url, {'isbn': self.book.isbn})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'ok')

        borrow.refresh_from_db()
        self.assertIsNotNone(borrow.returned_at)

    def test_return_book_missing_isbn(self):
        url = reverse('return book view')
        response = self.client.post(url, {})

        self.assertEqual(response.status_code, 400)

    def test_return_book_not_found(self):
        url = reverse('return book view')
        response = self.client.post(url, {'isbn': '9999999999999'})

        self.assertEqual(response.status_code, 404)

    def test_return_book_not_borrowed(self):
        url = reverse('return book view')
        response = self.client.post(url, {'isbn': self.book.isbn})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['message'], "User didn't borrow specified book before")

    def test_return_book_already_returned(self):
        # Create a borrow that's already returned
        borrow = Borrow.objects.create(
            user=self.user,
            book=self.book,
            returned_at=datetime.datetime.now()
        )

        url = reverse('return book view')
        response = self.client.post(url, {'isbn': self.book.isbn})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'User already returned specified book')
