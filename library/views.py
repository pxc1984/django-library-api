import enum

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest
from jwt import ExpiredSignatureError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from library.models import Book
from library.services.books import list_books, add_or_increase_book


@api_view(['GET', 'POST'])
def books_view(request):
    if request.method == 'GET':
        return Response({'books': list_books()}, status=HTTP_200_OK)
    elif request.method == 'POST':
        return _add_or_increase_book_view(request)
    else:
        return Response(status=HTTP_403_FORBIDDEN)


def _add_or_increase_book_view(request):
    # TODO: add checking for admin permissions

    book_info: dict[str, str | int]
    err_text: str
    book_info, err_text = _parse_book(request)
    if err_text is not None:
        return Response({'message': err_text}, status=HTTP_400_BAD_REQUEST)

    add_or_increase_book(book_info)

    return Response({'message': 'ok'}, status=HTTP_200_OK)


def _parse_book(request: WSGIRequest) -> tuple[dict[str, str | int], None] | tuple[None, str]:
    title = request.POST.get('title')
    if not title:
        return None, "Please provide book title"

    author = request.POST.get('author')
    if not author:
        return None, "Please provide book author"

    isbn = request.POST.get('isbn')
    if not isbn:
        return None, "Please provide book isbn"

    try:
        available_copies = int(request.POST.get('available_copies'))
        if not available_copies:
            return None, "Please provide available copies"
    except ValueError as e:
        return None, str(e)

    return {'title': title, 'author': author, 'isbn': isbn, 'available_copies': available_copies}, None
