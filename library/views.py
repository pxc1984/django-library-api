from library.services.books import list_books, add_or_increase_book

from dataclasses import dataclass
from typing import Optional
from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_405_METHOD_NOT_ALLOWED


@dataclass
class BookData:
    title: str
    author: str
    isbn: str
    available_copies: int


class BookValidator:
    ERROR_MESSAGES = {
        'missing_title': "Please provide book title",
        'missing_author': "Please provide book author",
        'missing_isbn': "Please provide book isbn",
        'missing_copies': "Please provide available copies"
    }

    @staticmethod
    def validate_request(request: HttpRequest) -> tuple[Optional[BookData], Optional[str]]:
        title = request.POST.get('title')
        if not title:
            return None, BookValidator.ERROR_MESSAGES['missing_title']

        author = request.POST.get('author')
        if not author:
            return None, BookValidator.ERROR_MESSAGES['missing_author']

        isbn = request.POST.get('isbn')
        if not isbn:
            return None, BookValidator.ERROR_MESSAGES['missing_isbn']

        try:
            available_copies = int(request.POST.get('available_copies'))
            if not available_copies:
                return None, BookValidator.ERROR_MESSAGES['missing_copies']
        except ValueError as e:
            return None, str(e)

        return BookData(
            title=title,
            author=author,
            isbn=isbn,
            available_copies=available_copies
        ), None


@api_view(['GET', 'POST'])
def books_view(request: HttpRequest) -> Response:
    if request.method == 'GET':
        return create_books_list_response()
    else: # elif request.method == 'POST':
        if not request.user.is_staff:
            return Response({'message': 'Admin privileges required'}, status=HTTP_403_FORBIDDEN)
        return handle_book_creation(request)


def create_books_list_response() -> Response:
    return Response({'books': list_books()}, status=HTTP_200_OK)


def handle_book_creation(request: HttpRequest) -> Response:
    book_data, err = BookValidator.validate_request(request)

    if err:
        return Response({'message': err}, status=HTTP_400_BAD_REQUEST)

    book_info = {
        'title': book_data.title,
        'author': book_data.author,
        'isbn': book_data.isbn,
        'available_copies': book_data.available_copies
    }
    add_or_increase_book(book_info)
    return Response({'message': 'ok'}, status=HTTP_200_OK)
