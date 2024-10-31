from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.UserCartView.as_view() ,name='cart_page'),
    path('checkout-shipping/', views.CartShippingView.as_view() ,name='cart_shipping_page'),
    path('checkout-payment/', views.CartPaymentView.as_view() ,name='cart_payment_page'),
    
    path('select-address/', views.SelectAddressView.as_view() ,name='select_address_page'),
    path('remove-address/', views.RemoveAddressView.as_view() ,name='remove_address_page'),
    
    path('change-order-count/', views.ChangeOrderCountView.as_view(), name='change_order_count_page'),
    path('remove-orders/', views.RemoveOrdersView.as_view(), name='remove_orders_page'),
    path('remove-order/', views.RemoveOrderView.as_view(), name='remove_order_page'),
    path('add-order/', views.AddOrderView.as_view(), name='add_order_page'),
    path('add-to-favorites/', views.AddToFavoritesView.as_view(), name='add_to_favorites_page'),
]