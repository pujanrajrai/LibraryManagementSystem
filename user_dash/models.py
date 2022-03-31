from django.db import models
from books.models import Book
from accounts.models import MyUser


# Create your models here.

class RequestBook(models.Model):
    books = models.ForeignKey(Book, on_delete=models.PROTECT)
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT)
    req_date = models.DateField(auto_now_add=True)
    is_req_cancelled = models.BooleanField(default=False)

    class Meta:
        unique_together = ['books', 'user', 'req_date']
