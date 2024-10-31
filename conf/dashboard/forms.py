from django import forms
from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'peer w-full rounded-lg bg-transparent p-2 placeholder-transparent outline-none focus:ring-0 xs:px-4 xs:py-3',
                'placeholder': ' ',
                'id': 'name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'peer w-full rounded-lg bg-transparent p-2 placeholder-transparent outline-none focus:ring-0 xs:px-4 xs:py-3',
                'placeholder': ' ',
                'id': 'family'
            }),
            'username': forms.TextInput(attrs={
                'class': 'peer w-full rounded-lg bg-transparent p-2 placeholder-transparent outline-none focus:ring-0 xs:px-4 xs:py-3',
                'placeholder': ' ',
                'id': 'username'
            }),
            'email': forms.TextInput(attrs={
                'class': 'peer w-full rounded-lg bg-transparent p-2 placeholder-transparent outline-none focus:ring-0 xs:px-4 xs:py-3',
                'placeholder': ' ',
                'id': 'email'
            }),
        }
        
        error_messages = {
            'first_name': {
                'required': 'لطفاً نام خود را وارد کنید.',
            },
            'last_name': {
                'required': 'لطفاً نام خانوادگی خود را وارد کنید.',
            },
            'username': {
                'required': 'لطفاً نام کاربری را وارد کنید.',
                'unique': 'این نام کاربری قبلاً ثبت شده است. لطفاً یک نام کاربری دیگر انتخاب کنید.',
            },
            'email': {
                'required': 'لطفاً ایمیل خود را وارد کنید.',
                'unique': 'این ایمیل قبلاً ثبت شده است. لطفاً یک ایمیل دیگر وارد کنید.',
            },
        }