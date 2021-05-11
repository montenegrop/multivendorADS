from versatileimagefield.fields import VersatileImageField, PPOIField

from django.db import models
from saleor.core.models import ModelWithMetadata, SortableModel

# Create your models here.


class VendorLocation(models.Model):
    country = models.CharField(max_length=3, blank=True, default='AR')
    province = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=40, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    lat = models.CharField(max_length=20, blank=True)
    lon = models.CharField(max_length=20, blank=True)


class Vendor(ModelWithMetadata):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=55, unique=True, allow_unicode=True)
    relevance = models.IntegerField(default=0)
    main_image = VersatileImageField(
        upload_to="vendor-main", blank=True, null=True
    )

    # fields for "empresa":
    description = models.TextField(blank=True)
    bussiness = models.TextField(blank=True)
    founding_year = models.IntegerField(null=True, blank=True)
    total_employess = models.IntegerField(null=True, blank=True)
    quality_norms = models.CharField(max_length=70, blank=True)
    open_hours = models.CharField(max_length=70, blank=True)
    billing = models.CharField(max_length=70, blank=True)

    # fields for "contacto":
    website_url = models.CharField(max_length=90, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    address = models.CharField(max_length=40, blank=True)

    # fields de ubicacion:
    location = models.ForeignKey(VendorLocation, on_delete=models.CASCADE, null=True)


class VendorContact(models.Model):
    Vendor = models.ForeignKey(
        Vendor, related_name="contacts", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    email = models.CharField(max_length=60, blank=True)

    SALES = 'sales'
    PURCHASING = 'purchasing'
    INDEFINITE = 'indefinite'

    ROLES = [
        ('', 'none'),
        (SALES, 'sales'),
        (PURCHASING, 'purchasing'),
        (INDEFINITE, 'any'),
    ]
    role = models.CharField(
        max_length=30,
        choices=ROLES,
        blank=True
    )


class VendorImage(SortableModel):
    vendor = models.ForeignKey(
        Vendor, related_name="images", on_delete=models.CASCADE
    )
    image = VersatileImageField(upload_to="vendors", ppoi_field="ppoi", blank=True)
    ppoi = PPOIField()
    alt = models.CharField(max_length=128, blank=True)
    title = models.CharField(max_length=25, blank=True)

    class Meta:
        ordering = ("sort_order", "pk")
        app_label = "vendors"

    def get_ordering_queryset(self):
        return self.vendor.images.all()
