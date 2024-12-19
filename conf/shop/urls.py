from django.urls import path
from . import views

urlpatterns = [
    path('product/<str:slug>/', views.ProductDetailView.as_view(), name='product_detail_page'),
    
    path('categories/', views.CategoriesView.as_view(), name='categories_page'),
    path('special_sale/', views.SpecialSaleView.as_view(), name='special_sale_page'),
    
    path('filter/', views.ProductsFilterView.as_view(), name='filter_products_page'),
]