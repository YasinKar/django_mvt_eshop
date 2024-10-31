from django.views.generic import TemplateView, View, ListView
from django.db.models import Q, Case, When, F, DecimalField, Sum
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import SiteSlider, Story, SiteBanner
from shop.models import Product, Category, Brand
from cart.models import Cart
from site_setting.models import SiteSetting, ElectronicSymbol

@method_decorator(cache_page(60 * 15), name='dispatch')
class HomeView(TemplateView):
    template_name = 'home/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['sliders'] = SiteSlider.objects.filter(is_active=True)
        
        context['banners'] = SiteBanner.objects.filter(is_active=True)[:2]
        
        context['stories'] = Story.objects.select_related('product').filter(is_active=True)
        
        context['categories'] = Category.objects.select_related('parent').filter(parent=None, is_active=True)
        
        context['brands'] = Brand.objects.filter(is_active=True)
        
        context['new_products'] = Product.objects.filter(is_active=True).order_by('-id')[:20]
        
        context['discounted_products'] = Product.objects.filter(is_active=True, is_sale=True).order_by('-id')[:20]
        
        context['best_seller_products'] = Product.objects.filter(is_active=True, inventory=1).order_by('-id')[:20]
        
        return context

class SearchView(ListView):
    template_name = 'home/search.html'
    context_object_name = 'results' 
    model = Product
    paginate_by = 30

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            search_history = self.request.session.get('search_history', [])
            
            if query not in search_history:
                search_history.insert(0, query)
                self.request.session['search_history'] = search_history
            
            return Product.objects.filter(
                Q(name__icontains=query) |
                Q(tags__tag__icontains=query) |
                Q(brand__name__icontains=query) |
                Q(category__name__icontains=query)
            ).distinct()
        else:
            return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')
        context['query'] = query
        return context

class ClearSearchHistoryView(View):
    def get(self, request, *args, **kwargs):
        request.session['search_history'] = []
        messages.success(request, 'تاریخچه جستوجوی شما با موفقیت پاک شد.')
        return redirect('home_page')

#components
def site_setting(request):
    site_setting = SiteSetting.objects.filter(is_main_setting=True).first()
    return {
        'site_setting': site_setting,
    }
    
class HeaderPartialView(TemplateView):
    template_name = 'shared/components/site_header.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
                
        context['categories'] = Category.objects.select_related('parent').filter(is_active=True)
        
        context['brands'] = Brand.objects.filter(is_active=True)
        
        search_history = self.request.session.get('search_history', [])
        
        search_history = search_history[:5]

        self.request.session['search_history'] = search_history

        context['recent_searches'] = self.request.session.get('search_history', [])
        
        if self.request.user.is_authenticated:
            user_cart, created = Cart.objects.get_or_create(user=self.request.user, is_paid=False)
            
            cart = (
                Cart.objects
                .filter(id=user_cart.id)
                .select_related('offer_code', 'user', 'address')
                .prefetch_related('orders__product', 'orders__color')
                .annotate(
                    get_total_amount=Sum(
                        Case(
                            When(orders__product__is_sale=True, 
                                then=F('orders__product__sale_price') * F('orders__count')),
                            default=F('orders__product__price') * F('orders__count'),
                            output_field=DecimalField()
                        )
                    )
                )
                .first()
            )
            
            context['cart'] = cart
        
        return context
    
class FooterPartialView(TemplateView):
    template_name = 'shared/components/site_footer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
                
        context['symbols'] = ElectronicSymbol.objects.filter(is_active=True)
        
        return context