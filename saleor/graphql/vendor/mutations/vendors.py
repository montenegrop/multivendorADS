import graphene
from saleor.vendors.models import Vendor


class VendorInput(graphene.InputObjectType):
    description = graphene.String(description="Vendor description (HTML/text).")
    name = graphene.String(description="Vendor name.")
    slug = graphene.String(description="Vendor slug.")
