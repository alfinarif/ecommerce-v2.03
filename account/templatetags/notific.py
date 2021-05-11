from django import template
from coupon.models import Notification, Message

register = template.Library()


@register.filter
def notific_count(user):
    notific_obj = Notification.objects.get(user=user)
    message_obj = Message.objects.filter(notification=notific_obj.id)
    return message_obj.count()


@register.filter
def notific_view(user):
    notific_obj = Notification.objects.get(user=user)
    message_obj = Message.objects.filter(notification=notific_obj.id)[:3]
    return message_obj
