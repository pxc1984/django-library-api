from django.urls import path

from library.views import books_view

urlpatterns = [
    path('books/', books_view, name='books view'),
    # path('borrow/', ),
    # path('return/', ),
    # path('borrows/', ),
]
