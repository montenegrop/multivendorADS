from django.db import models
from saleor.core.models import ModelWithMetadata
from versatileimagefield.fields import VersatileImageField

# Create your models here.


class Vendor(ModelWithMetadata):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=55, unique=True, allow_unicode=True)
    description = models.TextField(blank=True)
    relevance = models.IntegerField(default=0)
    main_image = VersatileImageField(
        upload_to="vendor-main", blank=True, null=True
    )
