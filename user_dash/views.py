from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Case, When
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView

from books.models import Book, LendBook, BookCopies
from profiles.models import Profiles
from .forms import ProfileForms, ProfileUpdateForm
from .models import RequestBook
from datetime import date
from decorator import is_user


@method_decorator(is_user(), name='dispatch')
class BookListView(ListView):
    model = Book
    template_name = 'user_dash/books_list_view.html'
    context_object_name = 'books'


@method_decorator(is_user(), name='dispatch')
class MyBookLendHistory(ListView):
    model = LendBook
    template_name = 'user_dash/my_book_history.html'
    context_object_name = 'books'

    def get_queryset(self):
        books = LendBook.objects.filter(user=self.request.user)
        for book in books:
            if not book.is_return:
                diff_days = (((date.today() - book.date_of_issue)).days)
                if diff_days > 5:
                    book.fine = (diff_days - 5) * 5

        return books


@method_decorator(is_user(), name='dispatch')
class ViewRequestBook(ListView):
    model = RequestBook
    template_name = 'user_dash/my_book_request.html'
    context_object_name = 'books'

    def get_queryset(self):
        return RequestBook.objects.filter(user=self.request.user)


@is_user()
def request_book(request, pk):
    if request.method == 'GET':
        book_id = pk
        book = Book.objects.get(pk=book_id)
        book_copies = BookCopies.objects.filter(book__pk=book.pk).filter(is_book_available=True)
        if book_copies:
            req_count = RequestBook.objects.filter(user=request.user).filter(req_date=date.today()).count()
            if req_count < 3:
                try:
                    RequestBook.objects.create(
                        user=request.user,
                        books=book,
                    )
                except:
                    messages.error(request, 'cannot request same book twice')
                    return redirect('user_dash:request_book_list_view')
                messages.success(request, 'book requested successfully')
                return redirect('user_dash:request_book_list_view')
            else:
                messages.error(request, 'cannot request book more than 3 in one day')
                return redirect('user_dash:request_book_list_view')

        else:
            messages.error(request, 'cannot request book more than 3 in one day')
            return redirect('user_dash:book_list')


@method_decorator(login_required(), name='dispatch')
class CreateProfile(CreateView):
    form_class = ProfileForms
    template_name = 'user_dash/profile_create_update.html'

    def get_success_url(self):
        return reverse_lazy('user_dash:profile_list_view')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_id'] = self.request.user
        return kwargs

    def get(self, *args, **kwargs):
        if Profiles.objects.filter(user__email=self.request.user).exists():
            return redirect('user_dash:profile_list_view')
        return super(CreateProfile, self).get(*args, **kwargs)

# listing user profile
@method_decorator(login_required(), name='dispatch')
class ProfileListView(ListView):
    model = Profiles
    template_name = 'user_dash/profile_view.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        queryset = Profiles.objects.filter(user__email=self.request.user)
        return queryset

    def get(self, *args, **kwargs):
        if not Profiles.objects.filter(user__email=self.request.user).exists():
            return redirect('user_dash:profile_create')
        return super(ProfileListView, self).get(*args, **kwargs)


@method_decorator(login_required(), name='dispatch')
class ProfileUpdateView(UpdateView):
    form_class = ProfileUpdateForm
    success_url = "/userdash/profile/view/"
    template_name = 'user_dash/update_profile.html'

    def get_object(self, **kwargs):
        return Profiles.objects.get(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_id'] = self.request.user
        return kwargs
