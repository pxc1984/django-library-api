from django.urls import path

from library.views import books_view, borrow_book, return_book

urlpatterns = [
    path('books/', books_view, name='books view'),
    path('borrow/', borrow_book, name='borrow view'),
    path('return/', return_book, name='return book'),
    # path('borrows/', ),
]
