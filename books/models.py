from django.db import models

# Create your models here.
from accounts.models import MyUser


class Author(models.Model):
    full_name = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name


class BookCategory(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(max_length=300)

    def __str__(self):
        return self.name


class Book(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=500)
    category = models.ForeignKey(BookCategory, on_delete=models.PROTECT)
    publication_name = models.CharField(max_length=300, blank=True, null=True)
    publication_date = models.DateField()

    def __str__(self):
        return self.title


class BookCopies(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    isbn = models.CharField(max_length=17, unique=True)
    rfid = models.CharField(max_length=20, unique=True, blank=True, null=True)
    is_book_lost = models.BooleanField(default=False)
    is_book_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.book.title} {self.isbn}'


class LendBook(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT)
    book = models.ForeignKey(BookCopies, on_delete=models.PROTECT)
    date_of_issue = models.DateField(auto_now_add=True)
    date_of_return = models.DateField(null=True, blank=True)
    fine = models.IntegerField(default=0)
    is_return = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} {self.book.book.title}'


