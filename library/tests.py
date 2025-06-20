from django.test import TestCase
from rest_framework.test import APITestCase


class BaseTestCase(APITestCase):
    def setUp(self):
        ...

class BookAPITest(BaseTestCase):
    ...

class BorrowAPITest(BaseTestCase):
    ...
