from django.urls import reverse

from library.models import Borrow
from library.tests.base import UserBookAPITest


class BorrowBookViewTestSet(UserBookAPITest):
    def test_borrow_book_missing_isbn(self):
        url = reverse('borrow book view')
        input_data = {

        }
        response = self.client.post(url, input_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], "Please provide book isbn")

    def test_borrow_book_book_not_found(self):
        url = reverse('borrow book view')
        response = self.client.post(url, {'isbn': '9999999999999'})
        self.assertEqual(response.status_code, 404)

    def test_borrow_book_no_available_copies(self):
        url = reverse('borrow book view')
        self.book.available_copies = 0
        self.book.save()
        response = self.client.post(url, {'isbn': self.book.isbn})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "Test Book by Test Author. ISBN: 1234567890123. isn't available.")

    def test_borrow_book_already_borrowed(self):
        url = reverse('borrow book view')
        borrow = Borrow.objects.create(user=self.user, book=self.book)
        response = self.client.post(url, {'isbn': self.book.isbn})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'],
                         f"User has already borrowed Test Book by Test Author. ISBN: 1234567890123. and cannot borrow twice: {str(borrow)}")

    def test_borrow_book_successful(self):
        url = reverse('borrow book view')
        response = self.client.post(url, {'isbn': self.book.isbn})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "ok")
        self.assertEqual(Borrow.objects.filter(user=self.user, book=self.book).count(), 1)
