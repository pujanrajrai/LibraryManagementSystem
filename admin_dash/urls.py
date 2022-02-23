from django.urls import path
from . import views

app_name = 'admin_dash'

urlpatterns = [
    path('', views.home, name='home'),
    # users
    path('add/users/', views.UsersCreateView.as_view(), name='add_users'),
    path('view/users/', views.UserListView.as_view(), name='user_list_view'),
    # profile
    path('update/user/<str:pk>', views.UserUpdateView.as_view(), name='update_user'),
    path('verify/user/email/<str:email>', views.verify_email, name='verify_email'),
    path('verify/user/<str:email>', views.verify_user, name='verify_user'),
    path('profile/view/<str:pk>', views.ProfileListView.as_view(), name='profile_list_view'),
    path('profile/create/<str:pk>', views.CreateProfile.as_view(), name='create_profile'),
    path('profile/update/<str:pk>', views.ProfileUpdateView.as_view(), name='profile_update'),
    # books
    path('book/create/', views.BookCreateView.as_view(), name='book_create'),
    path('book/update/<str:pk>', views.BookUpdate.as_view(), name='book_update'),
    path('book/list/', views.BookListView.as_view(), name='book_list'),
    path('book/copies/create/<str:pk>', views.BookCopiesCreateView.as_view(), name='book_copies_create'),
    path('book/copies/view/<str:pk>', views.BookCopiesListView.as_view(), name='book_copies_list'),
    # lend book
    path('book/lend/student/', views.user_id, name='student'),
    path('book/student/book/', views.book, name='book'),
    path('book/lend/student/book/', views.user_book, name='user_book'),
    path('book/lend/student/book/conform', views.lend_book, name='lend_book'),
    path('book/return/', views.return_book, name='return_book'),
    path('book/return/conform/', views.return_conform, name='return_book_conform'),
    # request book
    path('book/request/view', views.RequestBookListView.as_view(), name='request_book_view'),
    path('book/request/cancel/<str:pk>', views.cancel_book_request, name='cancel_book_request'),
    #book history
    path('book/history/',views.MyBookLendHistory.as_view(),name='book_history')
]
