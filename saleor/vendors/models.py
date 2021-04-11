from django.db import models
from saleor.core.models import ModelWithMetadata

# Create your models here.


class Vendor(ModelWithMetadata):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=55, unique=True, allow_unicode=True)
    description = models.TextField(blank=True)
    relevance = models.IntegerField(default=0)
