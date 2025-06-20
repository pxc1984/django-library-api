from django.urls import path

from library.views import books_view, borrow_book, return_book, list_borrows

urlpatterns = [
    path('books/', books_view, name='books view'),
    path('borrow/', borrow_book, name='borrow book view'),
    path('return/', return_book, name='return book view'),
    path('borrows/', list_borrows, name='list borrows view'),
]
