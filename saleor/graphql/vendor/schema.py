import graphene
from django.db import transaction

from graphene_django.types import DjangoObjectType, ObjectType

from saleor.vendors.models import Vendor
from saleor.graphql.core.mutations import BaseMutation, ModelDeleteMutation, ModelMutation
from .mutations.vendors import VendorRegister


class VendorType(DjangoObjectType):
    class Meta:
        description = "Vendors"
        model = Vendor


class VendorQueries(graphene.ObjectType):
    vendors = graphene.List(VendorType, description="list all vendors")

    def resolve_vendors(self, info, **kwargs):
        return Vendor.objects.all()


class VendorMutations(graphene.ObjectType):
    vendor_create = VendorRegister.Field()
