from versatileimagefield.fields import VersatileImageField, PPOIField

from django.db import models
from saleor.account.models import User
from saleor.vendors.models import Vendor
from saleor.product.models import BaseProduct
# Create your models here.


class ServiceContract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    service = models.ForeignKey(BaseProduct, on_delete=models.CASCADE)
    date = models.DateTimeField
    # 'YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]
    address = models.CharField(max_length=40, blank=False)
    localidad = models.CharField(max_length=30, blank=False)
    message = models.CharField(max_length=400, blank=False)
    stage = models.IntegerField(default=0)
    vendor_rejected = models.BooleanField(default=False)
    accepted_but_not_finished = models.BooleanField(default=False)
    user_reviewed = models.BooleanField(default=False)
    vendor_reviewed = models.BooleanField(default=False)
