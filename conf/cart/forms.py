from django import forms
from .models import Address, OfferCode

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'receiver_first_name',
            'receiver_last_name',
            'phone',
            'national_code',
            'address',
            'province',
            'city',
            'building_number',
            'building_unit',
            'post_code',
        ]
        widgets = {
            'receiver_first_name': forms.TextInput(attrs={
                'id': 'name',
                'class': 'peer w-full rounded-lg bg-transparent p-2 placeholder-transparent outline-none focus:ring-0 xs:px-4 xs:py-3',
                'placeholder': ' ',
            }),
            'receiver_last_name': forms.TextInput(attrs={
                'id': 'family',
                'class': 'peer w-full rounded-lg bg-transparent p-2 placeholder-transparent outline-none focus:ring-0 xs:px-4 xs:py-3',
                'placeholder': ' ',
            }),
            'phone': forms.TextInput(attrs={
                'id': 'phone',
                'class': 'peer w-full rounded-lg bg-transparent p-2 placeholder-transparent outline-none focus:ring-0 xs:px-4 xs:py-3',
                'placeholder': ' ',
            }),
            'national_code': forms.TextInput(attrs={
                'id': 'nCode',
                'class': 'peer w-full rounded-lg bg-transparent p-2 placeholder-transparent outline-none focus:ring-0 xs:px-4 xs:py-3',
                'placeholder': ' ',
            }),
            'address': forms.Textarea(attrs={
                'id': 'address',
                'class': 'peer w-full resize-none rounded-lg bg-transparent p-2 placeholder-transparent outline-none focus:ring-0 xs:px-4 xs:py-3',
                'placeholder': ' ',
                'rows': 2,
            }),
            'province': forms.TextInput(attrs={
                'id': 'province',
                'class': 'peer w-full rounded-lg bg-transparent p-2 placeholder-transparent outline-none focus:ring-0 xs:px-4 xs:py-3',
                'placeholder': ' ',
            }),
            'city': forms.TextInput(attrs={
                'id': 'city',
                'class': 'peer w-full rounded-lg bg-transparent p-2 placeholder-transparent outline-none focus:ring-0 xs:px-4 xs:py-3',
                'placeholder': ' ',
            }),
            'building_number': forms.TextInput(attrs={
                'id': 'bNumber',
                'class': 'peer w-full rounded-lg bg-transparent p-2 placeholder-transparent outline-none focus:ring-0 xs:px-4 xs:py-3',
                'placeholder': ' ',
            }),
            'building_unit': forms.TextInput(attrs={
                'id': 'bUnit',
                'class': 'peer w-full rounded-lg bg-transparent p-2 placeholder-transparent outline-none focus:ring-0 xs:px-4 xs:py-3',
                'placeholder': ' ',
            }),
            'post_code': forms.TextInput(attrs={
                'id': 'pCode',
                'class': 'peer w-full rounded-lg bg-transparent p-2 placeholder-transparent outline-none focus:ring-0 xs:px-4 xs:py-3',
                'placeholder': ' ',
            }),
        }
        labels = {
            'receiver_first_name': 'نام گیرنده',
            'receiver_last_name': 'نام خانوادگی گیرنده',
            'phone': 'شماره تماس گیرنده',
            'national_code': 'کد ملی گیرنده',
            'address': 'نشانی گیرنده',
            'province': 'استان',
            'city': 'شهر',
            'building_number': 'پلاک',
            'building_unit': 'واحد',
            'post_code': 'کد پستی',
        }
        error_messages = {
            'receiver_first_name': {
                'required': 'وارد کردن نام گیرنده الزامی است.',
                'max_length': 'نام گیرنده نباید بیشتر از ۲۰۰ کاراکتر باشد.',
            },
            'receiver_last_name': {
                'required': 'وارد کردن نام خانوادگی گیرنده الزامی است.',
                'max_length': 'نام خانوادگی گیرنده نباید بیشتر از ۲۰۰ کاراکتر باشد.',
            },
            'phone': {
                'invalid': 'شماره تماس وارد شده معتبر نیست.',
                'required': 'وارد کردن شماره تماس الزامی است.',
            },
            'national_code': {
                'invalid': 'کد ملی وارد شده معتبر نیست.',
                'required': 'وارد کردن کد ملی الزامی است.',
            },
            'address': {
                'required': 'وارد کردن نشانی الزامی است.',
            },
            'province': {
                'required': 'وارد کردن استان الزامی است.',
            },
            'city': {
                'required': 'وارد کردن شهر الزامی است.',
            },
            'post_code': {
                'invalid': 'کد پستی وارد شده معتبر نیست.',
                'required': 'وارد کردن کد پستی الزامی است.',
            },
        }

class OfferCodeForm(forms.ModelForm):
    class Meta:
        model = OfferCode
        fields = ['code']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'peer w-full rounded-lg border-none bg-transparent px-4 py-3 text-right text-text placeholder:text-sm placeholder:duration-300 focus:outline-none focus:ring-offset-0 ltr:focus:placeholder:translate-x-2 rtl:focus:placeholder:-translate-x-2',
                'placeholder': 'کد تخفیف',
                'autocomplete': 'off',
            }),
        }
        labels = {
            'code': 'کد تخفیف',
        }
        help_texts = {
            'code': 'کد تخفیف خود را وارد کنید.',
        }

    def clean_code(self):
        code = self.cleaned_data.get('code')
        try:
            offer = OfferCode.objects.get(code=code)
        except OfferCode.DoesNotExist:
            raise forms.ValidationError('کد تخفیف معتبر نمی‌باشد.')

        if not offer.is_valid():
            raise forms.ValidationError('کد تخفیف منقضی شده یا ظرفیت استفاده آن به پایان رسیده است.')

        return code