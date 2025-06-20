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
