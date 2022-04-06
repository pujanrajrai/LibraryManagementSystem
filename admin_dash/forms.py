from django import forms
from django.contrib.auth.hashers import make_password
from accounts.models import MyUser
from profiles.models import Profiles
from books.models import Book, BookCopies


class UsersForms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UsersForms, self).__init__(*args, **kwargs)
        self.fields['is_email_verified'].initial = True
        self.fields['is_user_verified'].initial = True

    class Meta:
        model = MyUser
        fields = ['email', 'password', 'is_email_verified', 'is_staff_member', 'is_user_verified']
        labels = {'email': 'Email'}
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_password(self):
        password = self.cleaned_data['password']
        special_sym = ['$', '@', '#', '%']

        if not any(char.isdigit() for char in password):
            raise forms.ValidationError('Password should have at least one numeral')

        if not any(char.isupper() for char in password):
            raise forms.ValidationError('Password should have at least one uppercase letter')

        if not any(char.islower() for char in password):
            raise forms.ValidationError('Password should have at least one lowercase letter')

        if not any(char in special_sym for char in password):
            raise forms.ValidationError('Password should have at least one of the symbols $@#')
        return make_password(self.cleaned_data['password'])


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = ['user', 'profile_image', 'full_name', 'address', 'phone_number', 'dob', 'gender',
                  'rf_id']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'rf_id': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(ProfileCreateForm, self).__init__(*args, **kwargs)
        self.fields['gender'].empty_label = 'Select Gender'
        self.fields['user'].empty_label = None
        self.fields['user'].queryset = MyUser.objects.filter(id=user)


class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = ['user', 'profile_image', 'full_name', 'address', 'phone_number', 'dob', 'gender',
                  'rf_id']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'rf_id': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(ProfileUpdate, self).__init__(*args, **kwargs)
        self.fields['gender'].empty_label = 'Select Gender'
        self.fields['user'].empty_label = None
        self.fields['user'].queryset = MyUser.objects.filter(id=user.user.id)


class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Select Category'

    class Meta:
        model = Book
        fields = ['author', 'title', 'category', 'publication_name', 'publication_date']
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'publication_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'publication_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BookCopiesForm(forms.ModelForm):
    def __init__(self, book_id, *args, **kwargs):
        super(BookCopiesForm, self).__init__(*args, **kwargs)
        self.fields['book'].empty_label = None
        self.fields['book'].queryset = Book.objects.filter(pk=book_id)

    class Meta:
        model = BookCopies
        fields = ['book', 'isbn', 'rfid']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'rfid': forms.TextInput(attrs={'class': 'form-control', 'required': 'false'}),
        }
