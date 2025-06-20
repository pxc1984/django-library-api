import datetime

from library.models import Book, Borrow
from library.services.books import list_books, add_or_increase_book, BookValidator, BookValidatorMode, \
    get_actual_available_copies

from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_405_METHOD_NOT_ALLOWED, \
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND


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


@api_view(['POST'])
def borrow_book(request: HttpRequest) -> Response:
    queried_book, err_response = BookValidator.get_queried_book_by_request(request)
    if err_response:
        return err_response
    if get_actual_available_copies(queried_book) < 1:
        return Response({'message': f"{str(queried_book)} isn't available."}, status=HTTP_200_OK)

    borrow = Borrow.objects.filter(user=request.user, book=queried_book).first()
    if borrow:
        return Response(
            {'message': f"User has already borrowed {str(queried_book)} and cannot borrow twice: {str(borrow)}"},
            status=HTTP_200_OK)

    Borrow.objects.create(
        user=request.user,
        book=queried_book,
    ).save()

    return Response({'message': 'ok'}, status=HTTP_200_OK)


@api_view(['POST'])
def return_book(request: HttpRequest) -> Response:
    queried_book, err_response = BookValidator.get_queried_book_by_request(request)
    if err_response:
        return err_response
    borrow = Borrow.objects.filter(user=request.user, book=queried_book).first()
    if not borrow:
        return Response({'message': 'User didn\'t borrow specified book before'}, status=HTTP_404_NOT_FOUND)
    if borrow.returned_at:
        return Response({'message': 'User already returned specified book'}, status=HTTP_400_BAD_REQUEST)
    borrow.returned_at = datetime.datetime.now()
    borrow.save()

    return Response({'message': 'ok'}, status=HTTP_200_OK)


@api_view(['GET'])
def list_borrows(request: HttpRequest) -> Response:
    if not request.user.is_staff:
        return Response({'message': 'Admin privileges required'}, status=HTTP_403_FORBIDDEN)
    return Response({'list': [str(borrow) for borrow in Borrow.objects.filter(returned_at__isnull=True)]},
                    status=HTTP_200_OK)
