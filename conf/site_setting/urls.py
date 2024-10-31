from django.urls import path
from . import views

urlpatterns = [
    path('contact-us/', views.ContactUsView.as_view(), name='contact_us_page'),
    path('rules/', views.SiteRulesView.as_view(), name='rules_page'),
    path('about/', views.SiteAboutView.as_view(), name='about_page'),
]