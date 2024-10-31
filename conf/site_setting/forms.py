from django import forms
from .models import ContactUs
import re

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['phone', 'title', 'message']
        widgets = {
            'phone': forms.TextInput(attrs={
                'placeholder': 'شماره موبایل',
                'class': 'mb-2 w-full rounded-lg border bg-background px-4 py-2.5 outline-none duration-300 placeholder:duration-300 focus:border-primary focus:placeholder:-translate-x-2'
            }),
            'title': forms.TextInput(attrs={
                'placeholder': 'عنوان',
                'class': 'mb-2 w-full rounded-lg border bg-background px-4 py-2.5 outline-none duration-300 placeholder:duration-300 focus:border-primary focus:placeholder:-translate-x-2'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'پیام',
                'rows': 4,
                'class': 'mb-2 w-full rounded-lg border bg-background px-4 py-2.5 outline-none duration-300 placeholder:duration-300 focus:border-primary focus:placeholder:-translate-x-2'
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        phone_regex = r"^(0|98)?([ ]|-|[()]){0,2}9[0-4|9]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}$"
        if not re.match(phone_regex, phone):
            raise forms.ValidationError({'phone': 'شماره موبایل وارد شده معتبر نیست.'})