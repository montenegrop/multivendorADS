from django.db import models
from saleor.account.models import User
from saleor.vendors.models import Vendor
from saleor.product.models import BaseProduct

from versatileimagefield.fields import PPOIField, VersatileImageField
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


CLIENT_UNAVAILABLE = 1
VENDOR_UNAVAILABLE = 2
JOB_NOT_POSSIBLE = 3
OTHER = 4

NO_COMPLETED = "No completa"


class VendorContractReview(models.Model):
    contract = models.ForeignKey(ServiceContract, on_delete=models.CASCADE)
    concreted = models.BooleanField(default=False)

    MOTIVES_CHOICES = [
        (CLIENT_UNAVAILABLE, "Cliente no disponible"),
        (VENDOR_UNAVAILABLE, "Prestador no se presenta"),
        (JOB_NOT_POSSIBLE, "Trabajo no realizable"),
        (OTHER, "Otro")
    ]

    motive = models.CharField(
        max_length=40, choices=MOTIVES_CHOICES, default=OTHER)

    other_motive = models.CharField(max_length=300, default=NO_COMPLETED)
    title = models.CharField(max_length=300, default=NO_COMPLETED)
    long_review = models.CharField(max_length=1000, default=NO_COMPLETED)


class VendorContractReviewGeneralImage(models.Model):
    image = VersatileImageField(
        upload_to="services",
        ppoi_field="ppoi",
        blank=True,
    )
    ppoi = PPOIField()
    alt = models.CharField(max_length=128, blank=True,
                           default="foto de review del prestador de servicio")


class VendorContractReviewImage(VendorContractReviewGeneralImage):
    vendor_contract_review = models.ForeignKey(
        VendorContractReview,
        related_name="vendor_contract_review_images",
        on_delete=models.CASCADE,
    )
    position = models.IntegerField()
