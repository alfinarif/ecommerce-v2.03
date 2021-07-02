from django.shortcuts import render, get_object_or_404, redirect
# messages
from django.contrib import messages
# login authentication
from django.contrib.auth.decorators import login_required
# models
from order.models import Cart, Order, Wishlist
from store.models import Product
from coupon.forms import CouponCodeForm
from coupon.models import Coupon

from decimal import Decimal

# for current time
from django.utils import timezone

# notification models
from notification.models import Notification



@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            #====== notification function ======
            sms = f"{item} Quantity has been updated"
            notify = Notification(item=item, user=request.user, notification_type=1,text_preview=sms)
            notify.save()
            #====== notification function ======
            messages.info(request, 'This item quantity was updated!')
            return redirect('index')
        else:
            order.orderitems.add(order_item[0])
            #====== notification function ======
            sms = f"{item} added to your cart!"
            notify = Notification(item=item, user=request.user, notification_type=1,text_preview=sms)
            notify.save()
            #====== notification function ======
            messages.info(request, 'This item was added to your cart!')
            return redirect('index')
    else:
        order = Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request, 'This item was added to your cart!')
        return redirect('index')


@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)

    if carts.exists() and orders.exists():
        orders = orders[0]
        coupon_form = CouponCodeForm(request.POST)
        if coupon_form.is_valid():
            current_time = timezone.now()
            code = coupon_form.cleaned_data.get('code')
            coupon_obj = Coupon.objects.get(code=code)
            if coupon_obj.valid_to >= current_time and coupon_obj.active == True:
                get_discount = (coupon_obj.discount / 100) * orders.get_totals()
                total_price_after_discount = orders.get_totals() - get_discount
                request.session['discount_total'] = total_price_after_discount
                request.session['coupon_code'] = code
                messages.success(request, f"{code} this coupon applied successfully!")
                return redirect('cart')
            else:
                coupon_obj.active = False
                coupon_obj.save()
                messages.warning(request, "This Coupon Code doesn't Active!")
                return redirect('cart')

        total_after_discount = request.session.get('discount_total')
        coupon_code = request.session.get('coupon_code')
        context = {
            'carts': carts,
            'orders': orders,
            'coupon_form': coupon_form,
            'coupon_code': coupon_code,
            'total_price_after_discount': total_after_discount
        }
        return render(request, 'order/cart.html', context)
    else:
        messages.info(request, "You haven't any item into your cart!")
        return redirect('index')


@login_required
def remove_item_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request, "This item was remove from your cart!")
            return redirect('cart')
        else:
            messages.info(request, "This item haven't in your cart!")
            return redirect('index')
    else:
        messages.warning(request, "You haven't active order!")
        return redirect('index')


@login_required
def increase_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f"{item.name} Quantity has been updated")
                return redirect('cart')
        else:
            messages.info(request, f"{item.name} is haven't in your cart!f")
            return redirect('index')
    else:
        messages.info(request, "You Haven't any active order!")
        return redirect('index')


@login_required
def decrease_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"{item.name} Quantity has been updated!")
                return redirect('cart')
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.name} Has been removed from your cart!")
                return redirect('cart')
        else:
            messages.info(request, f"{item.name} Haven't in your cart!")
            return redirect('index')
    else:
        messages.info(request, "You haven't any active order!")
        return redirect('index')


@login_required
def add_to_wishlist(request, pk):
    item = get_object_or_404(Product, pk=pk)
    wish_item = Wishlist.objects.filter(item=item, user=request.user, purchased=False)
    if wish_item.exists():
        if wish_item[0].quantity >= 1:
            messages.warning(request, f"{item.name} This item already Exists in your wishlist!")
            return redirect('index')
    else:
        Wishlist.objects.get_or_create(item=item, user=request.user, purchased=False)
        messages.info(request, "This item has been added to your Wishlist")
        return redirect('wishlist')


@login_required
def wishlist(request):
    wishlists = Wishlist.objects.filter(user=request.user, purchased=False).all()

    context = {
        'wishlists': wishlists
    }
    return render(request, 'order/wishlist.html', context)


@login_required
def delete_session_data(request):
    try:
        del request.session['discount_total']
        del request.session['coupon_code']
        return redirect('cart')
    except ValueError:
        pass
    return redirect('cart')
