from django.urls import reverse
from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    categoryname = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.categoryname)
        super().save(*args, **kwargs)

    def get_url(self):
            return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.categoryname
