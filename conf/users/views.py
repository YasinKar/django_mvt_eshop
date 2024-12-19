from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserLoginForm, OTPForm
from .models import OTP, User
from django.core.cache import cache
from .tasks import send_sms_task

#authentication
class LoginView(View):
    def get(self, request):
        form = UserLoginForm()
        context = {
            'form': form,
        }
        return render(request, 'auth/login.html', context)

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            
            print(phone)
            
            otp_obj = OTP.objects.create(phone=phone)
            otp_obj.generate_otp()
            
            # ارسال پیامک
            send_sms_task.delay(phone, otp_obj.otp)
                
            return redirect(reverse('verify_otp_page', kwargs={'phone': phone}))
    
        context = {
            'form': form,
        }
        return render(request, 'auth/login.html', context)

class VerifyOTPView(View):
    def get(self, request, *args, **kwargs):
        phone = self.kwargs['phone']
        
        form = OTPForm()
        
        context = {
            'form': form,
            'phone': phone,
        }
        return render(request, 'auth/verify_otp.html',  context)

    MAX_ATTEMPTS = 3  # Maximum attempts allowed
    BAN_DURATION = 120  # Duration in seconds for the ban (2 minutes)

    def post(self, request, *args, **kwargs):
        form = OTPForm(request.POST)
        phone = self.kwargs.get('phone')

        if form.is_valid():
            otp_code = form.get_otp()

            # Check if the user is banned
            ban_key = f'banned_{phone}'
            attempts_key = f'attempts_{phone}'
            attempts = cache.get(attempts_key, 0)

            if attempts >= self.MAX_ATTEMPTS:
                # Check if the ban duration has passed
                ban_time = cache.get(ban_key)
                if ban_time:
                    messages.error(request, 'تلاش شما برای ورود ناموفق بود, لطفا بعدا تلاش نمائید.')
                    return redirect(reverse('verify_otp_page', kwargs={'phone': phone}))
                else:
                    # Reset attempts if the ban duration has passed
                    cache.delete(attempts_key)
                    attempts = 0

            try:
                otp_obj = OTP.objects.get(phone=phone, otp=otp_code)

                # Check if OTP is valid (e.g., not expired)
                if not otp_obj.is_valid():
                    attempts += 1
                    cache.set(attempts_key, attempts, timeout=self.BAN_DURATION)
                    if attempts >= self.MAX_ATTEMPTS:
                        cache.set(ban_key, True, timeout=self.BAN_DURATION)
                    messages.error(request, 'کد یکبار مصرف نامعتبر است.')
                    return redirect(reverse('verify_otp_page', kwargs={'phone': phone}))

                # Check if user exists or create a new user
                user, created = User.objects.get_or_create(phone=phone, defaults={'username': phone})
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'شما با موفقیت وارد حساب خود شدید.')

                # Reset attempts after successful authentication
                cache.delete(attempts_key)

                return redirect(reverse('home_page'))

            except OTP.DoesNotExist:
                attempts += 1
                cache.set(attempts_key, attempts, timeout=self.BAN_DURATION)
                if attempts >= self.MAX_ATTEMPTS:
                    cache.set(ban_key, True, timeout=self.BAN_DURATION)
                messages.error(request, 'کد یکبار مصرف نامعتبر است.')
                return redirect(reverse('verify_otp_page', kwargs={'phone': phone}))
            
        context = {
            'form': form,
            'phone': phone,
        }
            
        return render(request, 'auth/verify_otp.html',  context)
        
class LogoutView(View):
    def get(self, request):
        logout(request)
        
        messages.success(request, 'شما با موفقیت از حساب خود خارج شدید.')
        return redirect(reverse('home_page'))