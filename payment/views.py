from django.shortcuts import render, HttpResponseRedirect, redirect, reverse

from django.http import JsonResponse

from django.conf import settings

from payment.forms import BillingAddressForm
from payment.models import BillingAddress
from order.models import Cart, Order

from django.contrib import messages

from django.contrib.auth.decorators import login_required

import json
from django.views.decorators.csrf import csrf_exempt


@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    form = BillingAddressForm(instance=saved_address)
    if request.method == 'POST':
        form = BillingAddressForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingAddressForm(instance=saved_address)
            messages.success(request, "Shipping Address has been saved")

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_total = order_qs[0].get_totals()
    total_after_discount = request.session.get('discount_total')
    coupon_code = request.session.get('coupon_code')

    context = {
        'form': form,
        'order_items': order_items,
        'order_total': order_total,
        'total_after_discount': total_after_discount,
        'coupon_code': coupon_code,
        'save_address': saved_address,
        'paypal_client_id': settings.PAYPAL_CLIENT_ID
    }

    return render(request, 'payment/checkout.html', context)


def payment(request):
    data = json.loads(request.body)
    print('Data Fetching->', data)
    order_id = data['order_id']
    payment_id = data['payment_id']
    status = data['status']
    if status == "COMPLETED":
        del request.session['discount_total']
        del request.session['coupon_code']
        if request.user.is_authenticated:
            order_qs = Order.objects.filter(user=request.user, ordered=False)
            order = order_qs[0]
            order.ordered = True
            order.orderId = order_id
            order.paymentId = payment_id
            order.save()
            cart_items = Cart.objects.filter(user=request.user, purchased=False)
            for item in cart_items:
                item.purchased = True
                item.save()
            return JsonResponse('Payment submitted..', safe=False)

    messages.warning(request, "Sorry Try again! your payment doesn't submited!")
    return redirect('index')
