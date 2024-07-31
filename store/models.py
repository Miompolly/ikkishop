from django.urls import reverse
from django.db import models
from dashboard.models import Category
from ikkishop import settings
from django.utils.text import slugify


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    slug= models.SlugField(max_length=200,unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='photos/products', blank=True)
    stock = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)

    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])
    def get_seller_phone_number(self):
        return self.user.phone_number if self.user else None
    


    def __str__(self):
        return self.product_name
        

