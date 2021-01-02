from django.db import models

# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=55, unique=True, allow_unicode=True)
    description = models.TextField(blank=True)