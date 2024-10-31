from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from .models import ContactUs
from .forms import ContactUsForm

class ContactUsView(CreateView):
    model = ContactUs
    form_class = ContactUsForm
    template_name = 'contact_us/contact_us.html'
    success_url = reverse_lazy('contact_us_page')

class SiteRulesView(TemplateView):
    template_name = 'rules/rules.html'
    
class SiteAboutView(TemplateView):
    template_name = 'about/about.html'