from django import forms

from accounts.models import MyUser
from profiles.models import Profiles


class ProfileForms(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = ['user', 'profile_image', 'full_name', 'address', 'phone_number', 'dob', 'gender']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, user_id, *args, **kwargs):
        super(ProfileForms, self).__init__(*args, **kwargs)
        self.fields['gender'].empty_label = 'Select Gender'
        self.fields['user'].empty_label = None
        self.fields['user'].queryset = MyUser.objects.filter(email=user_id)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = ['user', 'profile_image', 'full_name', 'address', 'phone_number', 'dob', 'gender']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'rf_id': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, user_id, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['gender'].empty_label = 'Select Gender'
        self.fields['user'].empty_label = None
        self.fields['user'].queryset = MyUser.objects.filter(email=user_id)
