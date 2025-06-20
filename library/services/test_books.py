from django.test import TestCase, RequestFactory
from library.services.books import BookData
from library.services.books import BookValidator, BookValidatorMode


class TestBookValidator(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_validate_request_missing_title(self):
        request = self.factory.post('/', {'author': 'Author', 'isbn': '1234567890', 'available_copies': '5'})
        data, error = BookValidator.validate_request(request, BookValidatorMode.All)
        self.assertIsNone(data)
        self.assertEqual(error, BookValidator.ERROR_MESSAGES['missing_title'])

    def test_validate_request_missing_author(self):
        request = self.factory.post('/', {'title': 'Title', 'isbn': '1234567890', 'available_copies': '5'})
        data, error = BookValidator.validate_request(request, BookValidatorMode.All)
        self.assertIsNone(data)
        self.assertEqual(error, BookValidator.ERROR_MESSAGES['missing_author'])

    def test_validate_request_missing_isbn(self):
        request = self.factory.post('/', {'title': 'Title', 'author': 'Author', 'available_copies': '5'})
        data, error = BookValidator.validate_request(request, BookValidatorMode.All)
        self.assertIsNone(data)
        self.assertEqual(error, BookValidator.ERROR_MESSAGES['missing_isbn'])

    def test_validate_request_missing_available_copies(self):
        request = self.factory.post('/', {'title': 'Title', 'author': 'Author', 'isbn': '1234567890'})
        data, error = BookValidator.validate_request(request, BookValidatorMode.All)
        self.assertIsNone(data)
        self.assertEqual(error, BookValidator.ERROR_MESSAGES['missing_copies'])

    def test_validate_request_invalid_available_copies(self):
        request = self.factory.post('/', {'title': 'Title', 'author': 'Author', 'isbn': '1234567890',
                                          'available_copies': 'invalid'})
        data, error = BookValidator.validate_request(request, BookValidatorMode.All)
        self.assertIsNone(data)
        self.assertIsNotNone(error)

    def test_validate_request_success(self):
        request = self.factory.post('/', {'title': 'Title', 'author': 'Author', 'isbn': '1234567890',
                                          'available_copies': '5'})
        data, error = BookValidator.validate_request(request, BookValidatorMode.All)
        self.assertIsInstance(data, BookData)
        self.assertIsNone(error)
        self.assertEqual(data.title, 'Title')
        self.assertEqual(data.author, 'Author')
        self.assertEqual(data.isbn, '1234567890')
        self.assertEqual(data.available_copies, 5)

    # And now with modes

    def test_validate_request_missing_title_mode(self):
        request = self.factory.post('/', {'author': 'Author', 'isbn': '1234567890', 'available_copies': '5'})
        data, error = BookValidator.validate_request(request, BookValidatorMode.NoTitle)
        self.assertIsInstance(data, BookData)
        self.assertIsNone(error)

    def test_validate_request_missing_author_mode(self):
        request = self.factory.post('/', {'title': 'Title', 'isbn': '1234567890', 'available_copies': '5'})
        data, error = BookValidator.validate_request(request, BookValidatorMode.NoAuthor)
        self.assertIsInstance(data, BookData)
        self.assertIsNone(error)

    def test_validate_request_missing_isbn_mode(self):
        request = self.factory.post('/', {'title': 'Title', 'author': 'Author', 'available_copies': '5'})
        data, error = BookValidator.validate_request(request, BookValidatorMode.NoIsbn)
        self.assertIsInstance(data, BookData)
        self.assertIsNone(error)

    def test_validate_request_missing_available_copies_mode(self):
        request = self.factory.post('/', {'title': 'Title', 'author': 'Author', 'isbn': '1234567890'})
        data, error = BookValidator.validate_request(request, BookValidatorMode.NoAvailableCopies)
        self.assertIsInstance(data, BookData)
        self.assertIsNone(error)

    def test_validate_request_invalid_available_copies_mode(self):
        request = self.factory.post('/', {'title': 'Title', 'author': 'Author', 'isbn': '1234567890',
                                          'available_copies': 'invalid'})
        data, error = BookValidator.validate_request(request, BookValidatorMode.NoAvailableCopies)
        self.assertIsInstance(data, BookData)
        self.assertIsNone(error)
