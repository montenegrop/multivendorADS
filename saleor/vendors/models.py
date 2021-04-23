from versatileimagefield.fields import VersatileImageField, PPOIField

from django.db import models
from saleor.core.models import ModelWithMetadata, SortableModel

# Create your models here.


class Vendor(ModelWithMetadata):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=55, unique=True, allow_unicode=True)
    relevance = models.IntegerField(default=0)
    main_image = VersatileImageField(
        upload_to="vendor-main", blank=True, null=True
    )

    # field for "empresa":
    description = models.TextField(blank=True)
    bussiness = models.TextField(blank=True)
    founding_year = models.ImageField(null=True)
    total_employess = models.ImageField(null=True)
    quality_norms = models.CharField(max_length=70)
    open_hours = models.CharField(max_length=70)
    billing = models.CharField(max_length=70, blank=True)


class VendorImage(SortableModel):
    vendor = models.ForeignKey(
        Vendor, related_name="images", on_delete=models.CASCADE
    )
    image = VersatileImageField(upload_to="vendors", ppoi_field="ppoi", blank=True)
    ppoi = PPOIField()
    alt = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ("sort_order", "pk")
        app_label = "vendors"

    def get_ordering_queryset(self):
        return self.vendor.images.all()
