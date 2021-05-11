from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='category')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created', ]
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    preview_des = models.TextField(max_length=200, verbose_name='Preview Description')
    description = models.TextField(max_length=1000, verbose_name='Description')
    image = models.ImageField(upload_to='products')
    price = models.FloatField()
    old_price = models.FloatField(default=0.00)
    is_stock = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_product_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created', ]
