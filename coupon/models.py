from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Coupon(models.Model):
    code = models.CharField(max_length=15, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Coupon"

    def __str__(self):
        return self.code


class Notification(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} Notifications"

    class Meta:
        verbose_name_plural = "Notifications"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance)
    instance.notification.save()


class Message(models.Model):
    notification = models.ManyToManyField(Notification)
    message = models.TextField(max_length=300, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.message)

