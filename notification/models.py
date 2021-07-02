from django.db import models
from django.conf import settings

from store.models import Product
# Create your models here.


class Notification(models.Model):
    NOTIFICATION_TYPE = (
        (1, 'add'),
        (2, 'payment'),
    )

    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='noti_item', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='noti_to_user')
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPE)
    text_preview = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)