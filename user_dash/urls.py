from django.urls import path
from . import views

app_name = 'user_dash'

urlpatterns = [
    path('book/list/', views.BookListView.as_view(), name='book_list'),
    path('book/history/', views.MyBookLendHistory.as_view(), name='book_list_history'),
    path('book/request/view', views.ViewRequestBook.as_view(), name='request_book_list_view'),
    path('book/request/<str:pk>', views.request_book, name='request_book'),
    path('profile/create/', views.CreateProfile.as_view(), name='profile_create'),
    path('profile/view/', views.ProfileListView.as_view(), name='profile_list_view'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
]
