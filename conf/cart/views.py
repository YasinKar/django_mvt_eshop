from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, When, F, DecimalField, Sum
from django.views.generic import ListView
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404,  render
from django.urls import reverse

from .models import Cart, Order, Address, OfferCode
from shop.models import Product, ProductColor
from .forms import AddressForm, OfferCodeForm

# Cart Pages
class UserCartView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'cart/checkout.html'
    context_object_name = 'cart'
    
    def get_queryset(self):
        user_cart, created = Cart.objects.get_or_create(user=self.request.user, is_paid=False)
            
        cart = Cart.objects.filter(id=user_cart.id).select_related('offer_code', 'user', 'address') \
        .prefetch_related('orders__product', 'orders__color') \
        .annotate(
                get_total_amount=Sum(
                    Case(
                        When(orders__product__is_sale=True, 
                            then=F('orders__product__sale_price') * F('orders__count')),
                        default=F('orders__product__price') * F('orders__count'),
                        output_field=DecimalField()
                    )
                )
            ).first()
        
        return cart

class CartShippingView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddressForm()
        
        user_cart, created = Cart.objects.get_or_create(user=self.request.user, is_paid=False)
        cart = Cart.objects.filter(id=user_cart.id).select_related('offer_code', 'user', 'address') \
        .prefetch_related('orders__product', 'orders__color') \
        .annotate(
                get_total_amount=Sum(
                    Case(
                        When(orders__product__is_sale=True, 
                            then=F('orders__product__sale_price') * F('orders__count')),
                        default=F('orders__product__price') * F('orders__count'),
                        output_field=DecimalField()
                    )
                )
            ).first()
        
        addresses = Address.objects.filter(user=request.user)
        
        context = {
            'form' : form,
            'cart' : cart,
            'addresses' : addresses
        }
        
        if not cart.orders.exists():
            messages.error(request, 'شما هیج سفارشی در سبد خرید خود ثبت نکرده اید.')
            return redirect(reverse('cart_page'))
            
        return render(request, 'cart/checkout-shipping.html', context)

    def post(self, request):
        form = AddressForm(request.POST)
        
        user_cart, created = Cart.objects.get_or_create(user=self.request.user, is_paid=False)
        cart = Cart.objects.filter(id=user_cart.id).select_related('offer_code', 'user', 'address') \
        .prefetch_related('orders__product', 'orders__color') \
        .annotate(
                get_total_amount=Sum(
                    Case(
                        When(orders__product__is_sale=True, 
                            then=F('orders__product__sale_price') * F('orders__count')),
                        default=F('orders__product__price') * F('orders__count'),
                        output_field=DecimalField()
                    )
                )
            ).first()
        
        addresses = Address.objects.filter(user=request.user)
        
        context = {
            'form' : form,
            'cart' : cart,
            'addresses' : addresses
        }
        
        if not cart.orders.exists:
            messages.error(request, 'شما هیج سفارشی در سبد خرید خود ثبت نکرده اید.')
            return redirect(reverse('cart_page'))
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            cart.address = instance
            cart.save()
            messages.success(request, 'ادرس جدید برای شما ثبت گردید.')
            return redirect(reverse('cart_shipping_page'))
                        
        return render(request, 'cart/checkout-shipping.html', context)

class CartPaymentView(LoginRequiredMixin, View):
    def get(self, request):
        user_cart, created = Cart.objects.get_or_create(user=self.request.user, is_paid=False)
        cart = Cart.objects.filter(id=user_cart.id).select_related('offer_code', 'user', 'address') \
        .prefetch_related('orders__product', 'orders__color') \
        .annotate(
                get_total_amount=Sum(
                    Case(
                        When(orders__product__is_sale=True, 
                            then=F('orders__product__sale_price') * F('orders__count')),
                        default=F('orders__product__price') * F('orders__count'),
                        output_field=DecimalField()
                    )
                )
            ).first()
        
        form = OfferCodeForm(initial={'code': cart.offer_code})
        
        context = {
            'cart' : cart,
            'form' : form
        }
        
        if not cart.orders.exists():
            messages.error(request, 'شما هیج سفارشی در سبد خرید خود ثبت نکرده اید.')
            return redirect(reverse('cart_page'))
        
        if not cart.address:
            messages.error(request, 'لطفا ابتدا ادرس خود را وارد کنید.')
            return redirect(reverse('cart_shipping_page'))
            
        return render(request, 'cart/checkout-payment.html', context)
    
    def post(self, request):
        user_cart, created = Cart.objects.get_or_create(user=self.request.user, is_paid=False)
        cart = Cart.objects.filter(id=user_cart.id).select_related('offer_code', 'user', 'address') \
        .prefetch_related('orders__product', 'orders__color') \
        .annotate(
                get_total_amount=Sum(
                    Case(
                        When(orders__product__is_sale=True, 
                            then=F('orders__product__sale_price') * F('orders__count')),
                        default=F('orders__product__price') * F('orders__count'),
                        output_field=DecimalField()
                    )
                )
            ).first()
        
        form = OfferCodeForm(request.POST, initial={'code': cart.offer_code})
        
        if form.is_valid():
            code = OfferCode.objects.filter(code=form.cleaned_data['code']).first()
            if code:
                if code.is_valid():
                    cart.offer_code = code
                    cart.save()
                    messages.success(request, 'کد تخفیف با موفقیت اعمال شد.')
                else:
                    messages.error(request, 'کد تخفیف معتبر نمی‌باشد یا منقضی شده است.')
            else:
                messages.error(request, 'کد تخفیف پیدا نشد.')

        if not cart.orders.exists():
            messages.error(request, 'شما هیج سفارشی در سبد خرید خود ثبت نکرده اید.')
            return redirect(reverse('cart_page'))
        
        if not cart.address:
            messages.error(request, 'لطفا ابتدا آدرس خود را وارد کنید.')
            return redirect(reverse('cart_shipping_page'))
            
        context = {
            'cart': cart,
            'form': form
        }
        
        return render(request, 'cart/checkout-payment.html', context)

# Address
class SelectAddressView(LoginRequiredMixin, View):
    def get(self, request):
        address_id = request.GET.get('address_id')
        
        if not address_id:
            return JsonResponse({
                'status': 'error',
                'message': 'address ID not provided'
            })
            
        cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
        address = Address.objects.filter(id=address_id, user=request.user).first()
        
        if not address:
            return JsonResponse({
                'status': 'error',
                'message': 'address not found'
            })
        
        cart.address = address
        cart.save()
        messages.success(request, 'ادرس جدید برای شما ثبت گردید.')
        return redirect(reverse('cart_shipping_page'))        

class RemoveAddressView(LoginRequiredMixin, View):
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
        
        return redirect('cart_shipping_page')

# Cart (Add,Remove)
class ChangeOrderCountView(LoginRequiredMixin, View):
    def get(self, request):
        state = request.GET.get('state')
        slug = request.GET.get('slug')
        color_id = request.GET.get('color_id')
        
        if not state or not slug:
            return JsonResponse({
                'status': 'error',
                'message': 'state or slug not provided'
            })
        
        product = get_object_or_404(Product, slug=slug)
        cart, created = Cart.objects.get_or_create(user_id=request.user.id, is_paid=False)
        
        if color_id:
            color_exists = product.color.filter(id=color_id).exists()
            if not color_exists:
                return JsonResponse({
                    'status': 'error',
                    'message': 'color not found'
                })
            color = get_object_or_404(ProductColor, id=color_id)
        else:
            color = None
        
        try:
            order, created = Order.objects.get_or_create(cart=cart, product=product, color=color)
        except Order.DoesNotExist:
            order = None
        
        if not order:
            return JsonResponse({
                'status': 'error',
                'message': 'Order not found'
            })
        
        if state == 'increase':
            if order.count < product.inventory:
                order.count += 1
                order.save()
                messages.success(request, 'محصول با موفقیت به سبد خرید اضافه شد.')
            else:
                messages.error(request, 'شما بیشتر از حد مجاز به سبد خود اضافه کرده‌اید.')
        elif state == 'decrease':
            if order.count == 1:
                order.delete()
                messages.success(request, 'محصول از سبد خرید شما حذف شد.')
            else:
                order.count -= 1
                order.save()
                messages.success(request, 'تعداد محصول کاهش یافت.')
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid state'
            })

        return redirect(reverse('cart_page'))

class AddOrderView(LoginRequiredMixin, View):
    def get(self, request):
        slug = request.GET.get('slug')
        color_id = request.GET.get('color_id')
        
        if not slug:
            return JsonResponse({
                'status': 'error',
                'message': 'slug or color_id not provided'
            })
        
        product = get_object_or_404(Product, slug=slug)
            
        if color_id:
            color_exists = product.color.filter(id=color_id).exists()
            if not color_exists:
                return JsonResponse({
                    'status': 'error',
                    'message': 'color not found'
                })
            color = get_object_or_404(ProductColor, id=color_id)
        else:
            color = None
            
        cart, created = Cart.objects.get_or_create(user_id=request.user.id, is_paid=False)
        
        try:
            order, created = Order.objects.get_or_create(cart=cart, cart__is_paid=False, product=product, color=color)
        except Order.DoesNotExist:
            order = None
        
        if not order:
            return JsonResponse({
                'status': 'error',
                'message': 'Order not found'
            })
        
        if order.count < product.inventory:
            order.count += 1
            order.save()
            messages.success(request, 'محصول با موفقیت به سبد خرید اضافه شد.')
            return redirect(reverse('product_detail_page', kwargs={'slug': slug}))
        
        else:
            messages.error(request, 'شما بیشتر از حد مجاز به سبد خود اضافه کرده‌اید.')
            return redirect(reverse('product_detail_page', kwargs={'slug': slug}))

class RemoveOrderView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.GET.get('order_id')
        
        if not order_id:
            return JsonResponse({
                'status': 'error',
                'message': 'order ID not provided'
            })

        user_cart, created = Cart.objects.get_or_create(is_paid=False, user_id=request.user.id)
        order = Order.objects.filter(cart_id=user_cart.id, id=order_id).first()
        
        if not order:
            return JsonResponse({
                'error' : 'Order not found'
            })
    
        order.delete()
        messages.success(request, 'محصول از سبد شما حذف شد.')
        return redirect(reverse('cart_page'))

class RemoveOrdersView(LoginRequiredMixin, View):
    def get(self, request):
        user_cart, created = Cart.objects.get_or_create(is_paid=False, user_id=request.user.id)
        orders = Order.objects.filter(cart_id=user_cart.id)
        
        if not orders.exists:
            messages.error(request, 'شما هیج سفارشی در سبد خود ندارید.')
            return redirect(reverse('cart_page'))
    
        orders.delete()
        messages.success(request, 'سبد خرید شما خالی شد.')
        return redirect(reverse('cart_page'))
    
class AddToFavoritesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        
        favorites = request.session.get('favorites', [])

        if product_id not in favorites:
            favorites.append(product_id)
            request.session['favorites'] = favorites

        messages.success(request, 'محصول به لیست علاقه مندی ها اضافه شد.')
        return redirect('product_detail_page', product.slug)