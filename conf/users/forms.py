from django import forms
import re

class UserLoginForm(forms.Form):
    phone = forms.CharField(
        required=True,
        label='شماره موبایل',
        error_messages={
            'required': 'لطفا شماره موبایل خود را وارد کنید.',
            'invalid': 'شماره موبایل معتبر نمی‌باشد.',
        },
        widget=forms.TextInput(attrs={
            'class': 'peer w-full rounded-lg bg-transparent p-3 text-left placeholder-transparent outline-none focus:ring-0 xs:p-4',
            'placeholder': ' ',
            'id': 'phone',
            'dir': 'ltr',
            'type' : 'number'
        })
    )

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        
        phone_regex = r"^(0|98)?([ ]|-|[()]){0,2}9[0-4|9]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}$"
        if not re.match(phone_regex, phone):
            raise forms.ValidationError('شماره موبایل وارد شده معتبر نیست.')
        
        return phone
    
class OTPForm(forms.Form):
    otp_1 = forms.CharField(
        max_length=1, 
        widget=forms.TextInput(attrs={
            'class': 'otp-input h-14 w-14 rounded-lg border bg-muted text-center text-lg outline-none xs:h-16 xs:w-16 md:text-xl',
            'inputmode': 'numeric',
            'maxlength': '1'
        })
    )
    otp_2 = forms.CharField(
        max_length=1, 
        widget=forms.TextInput(attrs={
            'class': 'otp-input h-14 w-14 rounded-lg border bg-muted text-center text-lg outline-none xs:h-16 xs:w-16 md:text-xl',
            'inputmode': 'numeric',
            'maxlength': '1'
        })
    )
    otp_3 = forms.CharField(
        max_length=1, 
        widget=forms.TextInput(attrs={
            'class': 'otp-input h-14 w-14 rounded-lg border bg-muted text-center text-lg outline-none xs:h-16 xs:w-16 md:text-xl',
            'inputmode': 'numeric',
            'maxlength': '1'
        })
    )
    otp_4 = forms.CharField(
        max_length=1, 
        widget=forms.TextInput(attrs={
            'class': 'otp-input h-14 w-14 rounded-lg border bg-muted text-center text-lg outline-none xs:h-16 xs:w-16 md:text-xl',
            'inputmode': 'numeric',
            'maxlength': '1'
        })
    )
    
    otp_5 = forms.CharField(
        max_length=1, 
        widget=forms.TextInput(attrs={
            'class': 'otp-input h-14 w-14 rounded-lg border bg-muted text-center text-lg outline-none xs:h-16 xs:w-16 md:text-xl',
            'inputmode': 'numeric',
            'maxlength': '1'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        otp_code = ''.join([
            cleaned_data.get('otp_1', ''),
            cleaned_data.get('otp_2', ''),
            cleaned_data.get('otp_3', ''),
            cleaned_data.get('otp_4', ''),
            cleaned_data.get('otp_5', ''),
        ])

        if len(otp_code) != 5:
            raise forms.ValidationError('لطفاً کد تایید 5 رقمی را به طور صحیح وارد کنید')

        return cleaned_data

    def get_otp(self):
        cleaned_data = super().clean()
        otp_code = ''.join([
            cleaned_data.get('otp_1', ''),
            cleaned_data.get('otp_2', ''),
            cleaned_data.get('otp_3', ''),
            cleaned_data.get('otp_4', ''),
            cleaned_data.get('otp_5', ''),
        ])
        
        return otp_code