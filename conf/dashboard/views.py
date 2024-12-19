from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView, ListView, DetailView, View

from users.models import User
from cart.models import Cart, Address, Order
from shop.models import Product
from .models import Message
from cart.forms import AddressForm
from .forms import UserUpdateForm

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carts'] = Cart.objects.filter(user=self.request.user, is_paid=True).exclude(status='در انتظار پرداخت')[:2]
        context['messages'] = Message.objects.filter(user=self.request.user)
        return context
    
# Edit   
class DashboardEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'dashboard/dashboard_edit.html'
    success_url = reverse_lazy('dashboard_edit_page')

    def get_object(self, queryset=None):
        return self.request.user
        
# Orders
class DashboardOrdersView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'dashboard/dashboard_orders.html'
    context_object_name = 'orders'          

    def get_queryset(self):
        user_orders = Cart.objects.filter(user=self.request.user, is_paid=True).exclude(status='در انتظار پرداخت')
        return user_orders
    
class DashboardOrderDetailView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = 'dashboard/dashboard_order_detail.html'
    context_object_name = 'order'

    def get_object(self, queryset=None):
        user_orders = Cart.objects.filter(user=self.request.user, is_paid=True).exclude(status='در انتظار پرداخت')
        return user_orders.first()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = Order.objects.filter(cart=self.object)
        return context

# Messages
class DashboardMessagesView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'dashboard/dashboard_messages.html'
    context_object_name = 'messages'

    def get_queryset(self):
        messages = Message.objects.filter(user=self.request.user)
        return messages

class DashboardDeleteMessagesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        Message.objects.filter(user=request.user).delete()
        messages.success(request, "پیام های شما با موفقیت حذف شد.")
        return redirect('dashboard_messages_page')

# Addresses
class DashboardAddressesView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard_addresses.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = Address.objects.filter(user=self.request.user)
        context['form'] = AddressForm()
        return context

    def post(self, request, *args, **kwargs):
        form = AddressForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            messages.success(request, 'ادرس جدید برای شما ثبت گردید.')
            return redirect(reverse_lazy('dashboard_addresses_page'))
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)

class DashboardRemoveAddressView(LoginRequiredMixin, View):
    def get(self, request):
        address_id = request.GET.get('address_id')
        if not address_id:
            messages.error(request, "آدرس یافت نشد.")
            return redirect('dashboard_addresses_page')
        
        try:
            address = get_object_or_404(Address, id=address_id, user=request.user)
            address.delete()
            messages.success(request, "آدرس با موفقیت حذف شد.")
        except Exception as e:
            messages.error(request, "خطایی در هنگام حذف آدرس رخ داد.")
        
        return redirect('dashboard_addresses_page')

# Favorites
class DashboardFavoritesView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard_favorites.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favorites = self.request.session.get('favorites', [])
        products = Product.objects.filter(id__in=favorites)
        context['favorites'] = products
        return context

class RemoveFavoriteView(LoginRequiredMixin, View):
    def get(self, request):
        favorite_id = request.GET.get('favorite_id')
        favorites = self.request.session.get('favorites', [])
        
        if not favorite_id:
            messages.error(request, "محصول یافت نشد.")
            return redirect('dashboard_favorites_page')

        if favorite_id in favorites:
            favorites.remove(favorite_id)
            request.session['favorites'] = favorites
            messages.success(request, "محصول از لیست علاقه مندی های شما با موفقیت حذف شد.")
        else:
            messages.error(request, "محصول در لیست شما موجود نبود.")

        return redirect('dashboard_favorites_page')
    
class RemoveAllFavoriteView(LoginRequiredMixin, View):
    def get(self, request):
        if 'favorites' in request.session:
            request.session.pop('favorites') 
            messages.success(request, "لیست علاقه‌مندی‌های شما خالی شد.")
        else:
            messages.error(request, "لیست علاقه‌مندی‌های شما خالی است.")
        
        return redirect('dashboard_favorites_page')
    
# Partial Views
class DashboardSidebarPartialView(TemplateView):
    template_name = 'includes/sidebar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = User.objects.filter(id=self.request.user.id).first()
        context['carts'] = Cart.objects.filter(user=self.request.user, is_paid=True).exclude(status='در انتظار پرداخت')
        return context