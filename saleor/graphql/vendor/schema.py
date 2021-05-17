import graphene

from saleor.vendors.models import Vendor as VendorModel

from saleor.graphql.core.fields import (
    FilterInputConnectionField,
)

from saleor.graphql.vendor.types.vendors import Vendor, VendorSortingInput
from saleor.graphql.vendor.mutations.vendors import (
    VendorCreateOrUpdate,
    VendorLocationCreateOrUpdate,
    VendorImageCreate
)


class VendorQueries(graphene.ObjectType):
    vendors = FilterInputConnectionField(
        Vendor,
        description="list all vendors",
        sort_by=VendorSortingInput(description="Sort categories."))

    vendor = graphene.Field(
        Vendor,
        id=graphene.Argument(graphene.ID, description="ID of the vendor."),
        description="Look up a vendor by ID.",
    )

    def resolve_vendor(self, info, id=None, **kwargs):
        return graphene.Node.get_node_from_global_id(info, id, Vendor)

    def resolve_vendors(self, info, **kwargs):
        return VendorModel.objects.all()


class VendorMutations(graphene.ObjectType):
    vendor_create_or_update = VendorCreateOrUpdate.Field()
    vendor_location_create_or_update = VendorLocationCreateOrUpdate.Field()
    vendor_image_create_or_update = VendorImageCreate.Field()
