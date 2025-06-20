from django.urls import reverse

from library.models import Book, Borrow
from library.tests.base import BookAPITest


class ListBorrowsUserBookAPITest(BookAPITest):
    def setUp(self):
        self.user = self.admin_user
        super().setUp()

        # Create a test book
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            isbn='1234567890',
            available_copies=1
        )

        # Create test borrow
        self.active_borrow = Borrow.objects.create(
            user=self.user,
            book=self.book
        )

        # Create returned borrow
        self.returned_borrow = Borrow.objects.create(
            user=self.user,
            book=self.book,
            returned_at='2025-06-20 12:00:00'
        )

    def test_list_borrows_unauthorized(self):
        """Test that unauthorized users cannot access the endpoint"""
        self.unauthenticate()
        response = self.client.get(reverse('list borrows view'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'message': 'Admin privileges required'})

    def test_list_borrows_regular_user(self):
        """Test that regular users cannot access the endpoint"""
        self.authenticateAs(self.normal_user)
        response = self.client.get(reverse('list borrows view'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'message': 'Admin privileges required'})

    def test_list_borrows_admin(self):
        """Test that admin users can see active borrows"""
        self.authenticateAs(self.admin_user)
        response = self.client.get(reverse('list borrows view'))
        self.assertEqual(response.status_code, 200)

        # Should only include active (non-returned) borrows
        self.assertEqual(len(response.json()['list']), 1)

        # Verify the response contains the active borrow
        self.assertIn(str(self.active_borrow), response.json()['list'])

        # Verify the returned borrow is not included
        self.assertNotIn(str(self.returned_borrow), response.json()['list'])
