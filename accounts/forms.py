from django import forms
from django.core.exceptions import ValidationError

from .models import MyUser
from django.contrib.auth.hashers import make_password


class MyUserCreationForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['email', 'password']

    def clean_password(self):
        password1 = self.cleaned_data['password']
        special_sym = ['$', '@', '#', '%']

        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError('Password should have at least one numeral')

        if not any(char.isupper() for char in password1):
            raise forms.ValidationError('Password should have at least one uppercase letter')

        if not any(char.islower() for char in password1):
            raise forms.ValidationError('Password should have at least one lowercase letter')

        if not any(char in special_sym for char in password1):
            raise forms.ValidationError('Password should have at least one of the symbols $@#')
        return make_password(self.cleaned_data['password'])


class ChangePasswordForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ["password"]

    def clean_password(self):
        password1 = self.cleaned_data['password']
        special_sym = ['$', '@', '#', '%']

        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError('Password should have at least one numeral')

        if not any(char.isupper() for char in password1):
            raise forms.ValidationError('Password should have at least one uppercase letter')

        if not any(char.islower() for char in password1):
            raise forms.ValidationError('Password should have at least one lowercase letter')

        if not any(char in special_sym for char in password1):
            raise forms.ValidationError('Password should have at least one of the symbols $@#')
        return password1
