from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard_page'),
    
    path('edit/', views.DashboardEditView.as_view(), name='dashboard_edit_page'),
    
    path('orders/', views.DashboardOrdersView.as_view(), name='dashboard_orders_page'),
    path('order/<pk>', views.DashboardOrderDetailView.as_view(), name='dashboard_order_detail_page'),
    
    path('addresses/', views.DashboardAddressesView.as_view(), name='dashboard_addresses_page'),
    path('addresses/remove', views.DashboardRemoveAddressView.as_view(), name='dashboard_remove_address_page'),
    
    path('messages/', views.DashboardMessagesView.as_view(), name='dashboard_messages_page'),
    path('messages/remove/', views.DashboardDeleteMessagesView.as_view(), name='dashboard_delete_messages_page'),
    
    path('favorites/', views.DashboardFavoritesView.as_view(), name='dashboard_favorites_page'),
    path('favorites/remove/', views.RemoveFavoriteView.as_view(), name='remove_from_favorites_page'),
    path('favorites/remove-all/', views.RemoveAllFavoriteView.as_view(), name='remove_all_from_favorites_page'),
]