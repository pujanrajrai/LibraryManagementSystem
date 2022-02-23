from django.contrib import admin
from .models import Book, BookCategory, BookCopies, Author, LendBook

# Register your models here.
admin.site.register(Author)
admin.site.register(BookCategory)
admin.site.register(Book)
admin.site.register(BookCopies)
admin.site.register(LendBook)
