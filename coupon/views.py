from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from coupon.models import Coupon
from coupon.forms import CouponCodeForm


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponCodeForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code=code,
                                        active=True)
            request.session['coupon_id'] = coupon.id
        except ValueError:
            request.session['coupon_id'] = None
        return redirect('cart')
