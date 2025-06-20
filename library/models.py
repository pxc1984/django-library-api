from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length= 13, unique=True, primary_key=True)
    available_copies = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author}. ISBN: {self.isbn}."

    class Meta:
        db_table = 'books'
        verbose_name = 'Book'
        verbose_name_plural = "Books"

class Borrow(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    book = models.ForeignKey(Book, models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.user} borrowed {self.book} at {self.borrowed_at} and returned at {self.returned_at}"

    class Meta:
        db_table = 'borrows'
        verbose_name = 'Borrow'
        verbose_name_plural = 'Borrows'
