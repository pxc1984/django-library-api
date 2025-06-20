from django.urls import path

from library.views import list_books, add_new_book

urlpatterns = [
    path('books/', list_books, name='list all books'),
    path('books/', add_new_book, name='add new book'),
    # path('borrow/', ),
    # path('return/', ),
    # path('borrows/', ),
]
