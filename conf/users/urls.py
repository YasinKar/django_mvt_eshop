from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('verify_otp/<str:phone>/', views.VerifyOTPView.as_view(), name='verify_otp_page'),
    path('logout/', views.LogoutView.as_view(), name='logout_page'),    
]