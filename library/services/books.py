from dataclasses import dataclass
from enum import Enum
from typing import Optional

from django.http import HttpRequest

from library.models import Book


def list_books() -> list[str]:
    book_queryset = Book.objects.all()
    resp = [str(book) for book in book_queryset]
    return resp

def add_or_increase_book(book_info: dict[str, str | int]):
    query = Book.objects.filter(isbn=book_info['isbn'])
    if not query.exists():
        obj = Book.objects.create(**book_info)
    else:
        obj = query.first()
        obj.available_copies += book_info['available_copies']
    obj.save()


@dataclass
class BookData:
    title: str | None
    author: str | None
    isbn: str | None
    available_copies: int | None


class BookValidatorMode(Enum):
    All = 15
    TitleAuthor = 12
    IsbnAvailableCopies = 3

    Title = 8
    NoTitle = 7

    Author = 4
    NoAuthor = 11

    Isbn = 2
    NoIsbn = 13

    AvailableCopies = 1
    NoAvailableCopies = 14


class BookValidator:
    ERROR_MESSAGES = {
        'missing_title': "Please provide book title",
        'missing_author': "Please provide book author",
        'missing_isbn': "Please provide book isbn",
        'missing_copies': "Please provide available copies"
    }

    @staticmethod
    def validate_request(request: HttpRequest, mode: BookValidatorMode = BookValidatorMode.All) -> tuple[
        Optional[BookData], Optional[str]]:
        title = request.POST.get('title')
        if not title and mode.value & BookValidatorMode.Title.value:
            return None, BookValidator.ERROR_MESSAGES['missing_title']

        author = request.POST.get('author')
        if not author and mode.value & BookValidatorMode.Author.value:
            return None, BookValidator.ERROR_MESSAGES['missing_author']

        isbn = request.POST.get('isbn')
        if not isbn and mode.value & BookValidatorMode.Isbn.value:
            return None, BookValidator.ERROR_MESSAGES['missing_isbn']

        if mode.value & BookValidatorMode.AvailableCopies.value:
            try:
                available_copies = request.POST.get('available_copies')
                if not available_copies:
                    return None, BookValidator.ERROR_MESSAGES['missing_copies']
                available_copies = int(available_copies)
            except ValueError or TypeError:
                return None, BookValidator.ERROR_MESSAGES['missing_copies']
        else:
            available_copies = 0

        return BookData(
            title=title,
            author=author,
            isbn=isbn,
            available_copies=available_copies
        ), None
