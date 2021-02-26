import graphene
from graphene_django.types import DjangoObjectType, ObjectType

from saleor.vendors.models import Vendor


class VendorType(DjangoObjectType):
    class Meta:
        model = Vendor


class VendorQueries(ObjectType):
    vendors = graphene.List(VendorType, description="list all vendors")

    def resolve_vendors(self, info, **kwargs):
        return Vendor.objects.all()
