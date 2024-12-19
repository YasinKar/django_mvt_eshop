from django.urls import path
from .views import 

urlpatterns = [
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
    path('contents/', SiteContentsView.as_view(), name='site-contents'),
]