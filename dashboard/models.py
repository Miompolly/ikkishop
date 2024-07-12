from django.db import models



class Category(models.Model):
    categoryname = models.CharField(max_length=255)  
    description = models.TextField(max_length=255, blank=True)
    image = models.ImageField(upload_to='photos/categories', blank=True)

    def __str__(self):
        return self.categoryname
