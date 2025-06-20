import enum

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest
from jwt import ExpiredSignatureError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from library.models import Book


@api_view(['GET'])
def list_books(request):
    book_queryset = Book.objects.all()
    resp = {'books': []}
    for book in book_queryset:
        resp['books'].append(str(book))
    return Response(resp, status=HTTP_200_OK)


@api_view(['POST'])
def add_new_book(request):
    # TODO: add checking for admin permissions

    book_info: dict[str, str | int]
    err_text: str
    book_info, err_text = _parse_book(request)
    if err_text is not None:
        return Response({'message': err_text}, status=HTTP_400_BAD_REQUEST)

    query = Book.objects.filter(isbn=book_info['isbn'])
    if not query.exists():
        obj = Book.objects.create(**book_info)
    else:
        obj = query.first()
        obj.available_copies += book_info['available_copies']
    obj.save()

    return Response({'message': 'ok'}, status=HTTP_200_OK)


def _parse_book(request: WSGIRequest) -> tuple[dict[str, str | int], None] | tuple[None, str]:
    title = request.POST['title']
    if not title:
        return None, "Please provide book title"

    author = request.POST['author']
    if not author:
        return None, "Please provide book author"

    isbn = request.POST['isbn']
    if not isbn:
        return None, "Please provide book isbn"

    try:
        available_copies = int(request.POST['available_copies'])
        if not available_copies:
            return None, "Please provide available copies"
    except ValueError as e:
        return None, str(e)

    return {'title': title, 'author': author, 'isbn': isbn, 'available_copies': available_copies}, None
