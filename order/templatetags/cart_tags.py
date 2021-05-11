from django import template
from order.models import Order, Cart, Wishlist
from store.models import Category
from django.template import RequestContext

register = template.Library()


@register.filter
def wish_count(user):
    wish = Wishlist.objects.filter(user=user, purchased=False)
    if wish.exists():
        return wish.count()
    else:
        return 0


@register.filter
def cart_count(user):
    order = Order.objects.filter(user=user, ordered=False)
    if order.exists():
        return order[0].orderitems.count()
    else:
        return 0


@register.filter
def cart_total(user):
    order = Order.objects.filter(user=user, ordered=False)
    if order.exists():
        return order[0].get_totals()
    else:
        return 0


@register.filter
def cart_view(user):
    cart = Cart.objects.filter(user=user, purchased=False)[:2]
    if cart.exists():
        return cart
    else:
        return cart


@register.filter
def category(user):
    if user.is_authenticated:
        cat = Category.objects.all()
        return cat
