from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django_filters.views import FilterView
from shop.models import Product, Category, Brand, ProductColor
from .forms import CommentForm
from .filters import ProductFilter
from django.shortcuts import redirect
from django.db.models import Q
from django.http import Http404
from django.contrib import messages

# Product Detail
@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_object(self):
        product_slug = self.kwargs.get('slug')
        
        try:
            product = Product.objects\
                .select_related('category', 'brand')\
                .prefetch_related('colors', 'tags', 'images', 'informations', 'comments__user', 'comments__replies')\
                .get(slug=product_slug, is_active=True)
        except Product.DoesNotExist:
            raise Http404("محصول پیدا نشد")
        
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        related_products = Product.objects.filter(
            Q(category=product.category) | Q(tags__in=product.tags.all()) | Q(brand=product.brand),
            is_active=True
        ).exclude(id=product.id).distinct()[:20]

        context['related_products'] = related_products
        
        context['form'] = kwargs.get('form', CommentForm())
        
        return context
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = self.object
            comment.user = request.user
            comment.save()
            messages.success(request, 'نظر شما با موفقیت ثبت شد.')
            return redirect('product_detail_page', slug=self.object.slug)
        else:
            context = self.get_context_data(form=form)
            return self.render_to_response(context)
        
# Categories
@method_decorator(cache_page(60 * 15), name='dispatch')
class CategoriesView(TemplateView):
    template_name = 'shop/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['categories'] = Category.objects.filter(is_active=True).select_related('parent')
        context['brands'] = Brand.objects.filter(is_active=True)

        return context
    
# Product Filter
class ProductsFilterView(FilterView, ListView):
    model = Product
    template_name = 'shop/filter_products.html'
    context_object_name = 'products'
    filterset_class = ProductFilter
    paginate_by = 25

    def get_queryset(self):
        queryset = super().get_queryset()
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        queryset = filterset.qs.filter(is_active=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['filterset'] = self.filterset_class(self.request.GET, queryset=queryset)
        context['brands'] = Brand.objects.filter(is_active=True)
        context['categories'] = Category.objects.filter(is_active=True)
        context['colors'] = ProductColor.objects.all()
        return context

# Special Sale
@method_decorator(cache_page(60 * 15), name='dispatch')
class SpecialSaleView(ListView):
    model = Product
    template_name = 'shop/special_sale.html'
    context_object_name = 'products'
    paginate_by = 30

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True, is_sale=True)
        return queryset