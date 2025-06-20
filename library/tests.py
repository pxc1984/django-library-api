from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from library.models import Book, Borrow


class BaseBookTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create normal user
        cls.user = User.objects.create_user(
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

    def specificDataSetup(self):
        pass

    def setUp(self):
        self.sample_book = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'available_copies': 5
        }
        self.book = Book.objects.create(**self.sample_book)
        self.authenticate()
        self.specificDataSetup()

    def authenticate(self):
        """
        Helper function that authenticates as a self.user.
        :return:
        """
        self.client.force_authenticate(user=self.user)

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


class AdminBookAPIBookTest(BaseBookTestCase):
    def setUp(self):
        self.user = self.admin_user  # Use the admin user for these tests
        super().setUp()

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


class UserBookAPIBookTest(BaseBookTestCase):
    def setUp(self):
        super().setUp()
        # The default user from BaseBookTestCase will be used

    def test_add_new_book_wrong_permissions(self):
        response, new_book_data = self._add_new_book()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Book.objects.filter(isbn=new_book_data['isbn']).exists())

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


class BookAPIBookTest(BaseBookTestCase):
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


class BorrowAPITest(UserBookAPIBookTest):
    def specificDataSetup(self):
        test_book = Book.objects.filter(isbn='1234567890123').first()
        if test_book:
            test_book.delete()
        self.book = Book.objects.create(title='Test Book',
                                        author='Test Author',
                                        isbn='1234567890123',
                                        available_copies=5)

    def test_borrow_book_missing_isbn(self):
        url = reverse('borrow view')
        input_data = {

        }
        response = self.client.post(url, input_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], "Please provide book isbn")

    def test_borrow_book_book_not_found(self):
        url = reverse('borrow view')
        response = self.client.post(url, {'isbn': '9999999999999'})
        self.assertEqual(response.status_code, 404)

    def test_borrow_book_no_available_copies(self):
        url = reverse('borrow view')
        self.book.available_copies = 0
        self.book.save()
        response = self.client.post(url, {'isbn': self.book.isbn})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "Test Book by Test Author. ISBN: 1234567890123. isn't available.")

    def test_borrow_book_already_borrowed(self):
        url = reverse('borrow view')
        borrow = Borrow.objects.create(user=self.user, book=self.book)
        response = self.client.post(url, {'isbn': self.book.isbn})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'],
                         f"User has already borrowed Test Book by Test Author. ISBN: 1234567890123. and cannot borrow twice: {str(borrow)}")

    def test_borrow_book_successful(self):
        url = reverse('borrow view')
        response = self.client.post(url, {'isbn': self.book.isbn})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "ok")
        self.assertEqual(Borrow.objects.filter(user=self.user, book=self.book).count(), 1)


class ReturnAPITest(UserBookAPIBookTest):
    def specificDataSetup(self):
        test_book = Book.objects.filter(isbn='1234567890123').first()
        if test_book:
            test_book.delete()
        self.book = Book.objects.create(title='Test Book',
                                        author='Test Author',
                                        isbn='1234567890123',
                                        available_copies=5)

    def test_return_book_successful(self):
        borrow = Borrow.objects.create(user=self.user, book=self.book)

        url = reverse('return book')
        response = self.client.post(url, {'isbn': self.book.isbn})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'ok')

        borrow.refresh_from_db()
        self.assertIsNotNone(borrow.returned_at)
