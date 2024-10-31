from django import forms
from .models import ProductComment

class CommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['title', 'message', 'recommend', 'replay']
        error_messages = {
            'title': {
                'required': 'وارد کردن عنوان نظر الزامی است.',
                'max_length': 'عنوان نظر نباید بیشتر از ۲۰۰ کاراکتر باشد.',
            },
            'message': {
                'required': 'وارد کردن پیام نظر الزامی است.',
            },
            'recommend': {
                'required': 'وارد کردن پیشنهاد میکنم/نمیکنم الزامی است.',
            },
        }