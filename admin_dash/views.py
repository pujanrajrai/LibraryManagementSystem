from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from accounts.models import MyUser
from profiles.models import Profiles
from .forms import UsersForms, ProfileCreateForm, BookForm, BookCopiesForm, ProfileUpdate
from books.models import Book, BookCopies, LendBook
from datetime import date
from user_dash.models import RequestBook
from decorator import is_admin
from django.core.mail import send_mail
from LibraryManagementSystem.settings import EMAIL_HOST_USER


# from

# Create your views here.


# dashboard home
@is_admin()
def home(request):
    context = {
        'users': MyUser.objects.all().count(),
        'total_book': Book.objects.all().count(),
        'book_request': RequestBook.objects.all().count(),
        'book_lend': LendBook.objects.all().count(),
        'book_copies': BookCopies.objects.all().count(),
        'book_return': LendBook.objects.all().filter(is_return=True).count(),
    }

    return render(request, 'admin_dash/admin.html', context)


# create User
@method_decorator(is_admin(), name='dispatch')
class UsersCreateView(CreateView):
    form_class = UsersForms
    template_name = 'admin_dash/user_create_update.html'
    success_message = 'User Created Successfully'

    def get_success_url(self, **kwargs):
        users = MyUser.objects.last()
        return reverse_lazy('admin_dash:create_profile', kwargs={'pk': users.pk})


# update user
@method_decorator(is_admin(), name='dispatch')
class UserUpdateView(UpdateView):
    form_class = UsersForms
    model = MyUser
    template_name = 'admin_dash/user_create_update.html'
    success_message = 'User Created Successfully'

    def get_success_url(self, **kwargs):
        users = MyUser.objects.last()
        return reverse_lazy('admin_dash:user_list_view')


# list all users
@method_decorator(is_admin(), name='dispatch')
class UserListView(ListView):
    model = MyUser
    template_name = 'admin_dash/user_list_view.html'
    context_object_name = 'users'


# admin verifying email
@is_admin()
def verify_email(request, email):
    MyUser.objects.filter(email=email).update(is_email_verified=True)
    return redirect('admin_dash:user_list_view')


# admin Verify User
@is_admin()
def verify_user(request, email):
    MyUser.objects.filter(email=email).update(is_user_verified=True)
    return redirect('admin_dash:user_list_view')


# admin block user
@is_admin()
def block_user(request, email):
    MyUser.objects.filter(email=email).update(is_active=False)
    return redirect('admin_dash:user_list_view')


# viewing user profile
@method_decorator(is_admin(), name='dispatch')
class ProfileListView(ListView):
    model = Profiles
    template_name = 'admin_dash/profile_view.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        queryset = Profiles.objects.filter(user__pk=self.kwargs['pk'])
        return queryset

    def get(self, *args, **kwargs):
        if not Profiles.objects.filter(user__pk=self.kwargs['pk']).exists():
            return redirect(f'/admindash/profile/create/{self.kwargs["pk"]}')
        return super(ProfileListView, self).get(*args, **kwargs)


# creating user profile
@method_decorator(is_admin(), name='dispatch')
class CreateProfile(CreateView):
    form_class = ProfileCreateForm
    template_name = 'admin_dash/create_update_profile.html'
    success_url = '/profile/view/'

    def get_success_url(self):
        return reverse_lazy('admin_dash:user_list_view')

    def get(self, *args, **kwargs):
        print(MyUser.objects.filter(pk=self.kwargs['pk']))
        if Profiles.objects.filter(id=self.kwargs['pk']).exists():
            return redirect('profile:view_profile')
        return super(CreateProfile, self).get(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.kwargs['pk']
        return kwargs


# updating user profile
@method_decorator(is_admin(), name='dispatch')
class ProfileUpdateView(UpdateView):
    form_class = ProfileUpdate
    template_name = 'admin_dash/update_profile.html'
    queryset = Profiles.objects.all()
    success_url = "/profile/view"

    def get_success_url(self, **kwargs):
        return reverse_lazy('admin_dash:user_list_view')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = Profiles.objects.get(id=self.kwargs['pk'])
        return kwargs


# create book
@method_decorator(is_admin(), name='dispatch')
class BookCreateView(CreateView):
    form_class = BookForm
    template_name = 'admin_dash/book_create_update.html'

    def get_success_url(self):
        return reverse_lazy('admin_dash:book_list')


# update book
@method_decorator(is_admin(), name='dispatch')
class BookUpdate(UpdateView):
    form_class = BookForm
    model = Book
    template_name = 'admin_dash/book_create_update.html'

    def get_success_url(self):
        return reverse_lazy('admin_dash:book_list')


# book list view
@method_decorator(is_admin(), name='dispatch')
class BookListView(ListView):
    model = Book
    template_name = 'admin_dash/books_list_view.html'
    context_object_name = 'books'


# adding books
@method_decorator(is_admin(), name='dispatch')
class BookCopiesCreateView(CreateView):
    model = BookCopies
    form_class = BookCopiesForm
    template_name = 'admin_dash/book_copies_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['book_id'] = self.kwargs['pk']
        return kwargs

    def get_success_url(self):
        return reverse_lazy('admin_dash:book_list')


# viewing all the books present in database
@method_decorator(is_admin(), name='dispatch')
class BookCopiesListView(ListView):
    model = BookCopies
    template_name = 'admin_dash/books_copies_list_view.html'
    context_object_name = 'copies'

    def get_queryset(self):
        return BookCopies.objects.filter(book__pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_id'] = self.kwargs['pk']
        return context


# taking user rfid as input to identify the user
@is_admin()
def user_id(request):
    return render(request, 'admin_dash/student_indentify.html')


# verifying users with rfid
@is_admin()
def book(request):
    if request.method == 'POST':
        context = {}
        rfid = request.POST.get('rfid')
        try:
            profile = Profiles.objects.get(rf_id=rfid)
        except:
            profile = False
        if not profile:
            context['rfid'] = rfid
            context['errors'] = "user doesnot exist"
            return render(request, 'admin_dash/student_indentify.html', context)
        context['profile'] = profile
        return render(request, 'admin_dash/student_lend_book.html', context)


# checking if book exist or not with rfid or isbn
@is_admin()
def user_book(request):
    if request.method == 'POST':
        context = {}
        profile = Profiles.objects.get(rf_id=request.POST.get('rfid'))
        book_id = request.POST.get('book_id')
        book_isbn = BookCopies.objects.filter(isbn=book_id)
        book_rfid = BookCopies.objects.filter(rfid=book_id)
        context['profile'] = profile

        if book_isbn:
            book = BookCopies.objects.get(isbn=book_id)
        elif book_rfid:
            book = BookCopies.objects.get(rfid=book_id)
        else:
            context['errors'] = 'Book does not exist'

            return render(request, 'admin_dash/student_lend_book.html', context)
        context['book'] = book
        context['book_id'] = book.pk
        context['user_email'] = profile.user.email
        return render(request, 'admin_dash/student_book.html', context)


# lending book
@is_admin()
def lend_book(request):
    if request.method == 'POST':
        try:
            # checking if book existence
            books = BookCopies.objects.get(isbn=request.POST.get('isbn'))
            # checking if book is avialable
            if books.is_book_available:
                lend_book_count = LendBook.objects.filter(
                    user=MyUser.objects.get(email=request.POST.get('user'))).filter(is_return=False).count()
                # checking if user have taken book less then 6
                if lend_book_count < 6:
                    available_book_count = BookCopies.objects.filter(book=books.book).filter(
                        is_book_available=True).count()
                    req_book = RequestBook.objects.filter(books=books.book).filter(req_date=date.today()).filter(
                        is_req_cancelled=False)
                    # checking if book is not reserved
                    if not available_book_count > req_book.count():
                        is_eligible = req_book.filter(user=MyUser.objects.get(email=request.POST.get('user')))
                        # incase of book reserve check if the request user have reserved book
                        if is_eligible:
                            pass
                        else:
                            messages.error(request,
                                           'Book has been booked for today please cancel booking to lent this book')
                            return redirect('admin_dash:student')
                    # lending book
                    LendBook.objects.create(
                        user=MyUser.objects.get(email=request.POST.get('user')),
                        book=BookCopies.objects.get(isbn=request.POST.get('isbn'))
                    )
                    # making book as unavailable
                    BookCopies.objects.filter(isbn=request.POST.get('isbn')).update(is_book_available=False)
                    # sending mail
                    send_mail(
                        f"Hello {MyUser.objects.get(email=request.POST.get('user'))}",
                        f"You have taken {books.book.title} on {date.today()} please return it within 5 days to avoid "
                        f"fine",
                        EMAIL_HOST_USER,
                        [MyUser.objects.get(email=request.POST.get('user'))],
                    )
                else:
                    messages.error(request, 'Book Lent limit exceed more then 5')
                    return redirect('admin_dash:student')
                messages.success(request, 'Book Lent successfully')
                return redirect('admin_dash:student')
            else:
                messages.error(request, 'Make this book available first by returning or by canceling reservations')
                return redirect('admin_dash:student')
        except:
            messages.error(request, 'something went wrong')
            return redirect('admin_dash:student')


# confirm return
@is_admin()
def return_book(request):
    if request.method == 'POST':
        context = {}
        # check if book is taken or not
        book_isbn = LendBook.objects.filter(book__isbn=request.POST.get('book_id')).filter(is_return=False)
        book_rfid = LendBook.objects.filter(book__rfid=request.POST.get('book_id')).filter(is_return=False)
        # checking by isbn
        if book_isbn:
            # calculating fine
            # find difference between taken date and today date
            days = (date.today() - LendBook.objects.filter(book__isbn=request.POST.get('book_id')).get(
                is_return=False).date_of_issue).days
            # calculating fine for more then 5 days
            if days > 5:
                fine = (days - 5) * 5
            else:
                fine = 0

            context['book'] = book_isbn
        # checking by rfid
        elif book_rfid:
            days = (LendBook.objects.filter(book__rfid=request.POST.get('book_id')).get(
                is_return=False).date_of_issue - date.today()).days
            if days > 5:
                fine = (days - 5) * 5
            else:
                fine = 0
            context['book'] = book_rfid
        else:
            messages.error(request, 'no book was taken or book id does not exist')
            return redirect('admin_dash:return_book')
        context['fine'] = fine
        return render(request, 'admin_dash/conform_book_return.html', context)
    else:
        return render(request, 'admin_dash/return_book.html')


# return book successfully
@is_admin()
def return_conform(request):
    if request.method == 'POST':
        try:
            # finding the difference between todays date and book taken date
            days = (date.today() - LendBook.objects.filter(book__isbn=request.POST.get('book_id')).get(
                is_return=False).date_of_issue).days
            # checking if book difference date was less then 5
            if days > 5:
                fine = (days - 5) * 5
            else:
                fine = 0

            # book return successfully and adding fine
            LendBook.objects.filter(book__isbn=request.POST.get('book_id')).filter(is_return=False).update(
                is_return=True,
                date_of_return=date.today(),
                fine=fine
            )
            # making book avialable
            BookCopies.objects.filter(isbn=request.POST.get('book_id')).update(is_book_available=True)
            messages.success(request, 'Book Return Sucessfully')
            return redirect('admin_dash:return_book')
        except:
            messages.error(request, 'Request Not allowed')
            return redirect('admin_dash:return_book')


# view request book
@method_decorator(is_admin(), name='dispatch')
class RequestBookListView(ListView):
    model = RequestBook
    template_name = 'admin_dash/book_request.html'
    context_object_name = 'books'

    def get_queryset(self):
        return RequestBook.objects.all().order_by('-req_date')


# cancel book request
@is_admin()
def cancel_book_request(request, pk):
    try:
        RequestBook.objects.filter(pk=pk).update(is_req_cancelled=True)
        messages.success(request, 'Request Cancel')
    except:
        messages.error(request, 'Something went wrong')
    return redirect('admin_dash:request_book_view')


# view book lent history
@method_decorator(is_admin(), name='dispatch')
class MyBookLendHistory(ListView):
    model = LendBook
    template_name = 'admin_dash/book_history.html'
    context_object_name = 'books'

    def get_queryset(self):
        books = LendBook.objects.all().order_by('is_return')

        for book in books:
            # calculating fine
            if not book.is_return:
                diff_days = (((date.today() - book.date_of_issue)).days)
                if diff_days > 5:
                    book.fine = (diff_days - 5) * 5
        return books
