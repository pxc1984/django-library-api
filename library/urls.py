from django.urls import path

from library.views import books_view, borrow_book

urlpatterns = [
    path('books/', books_view, name='books view'),
    path('borrow/', borrow_book, name='borrow view'),
    # path('return/', ),
    # path('borrows/', ),
]
