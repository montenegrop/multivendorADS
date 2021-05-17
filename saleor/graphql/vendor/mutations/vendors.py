import graphene
from django.db import transaction

from saleor.graphql.vendor.schema import Vendor

from saleor.graphql.vendor.types.vendors import (
    VendorServiceImage,
    VendorImageCreateInput,
    VendorCreateOrUpdateInput
)
from saleor.graphql.core.utils import validate_image_file
from saleor.graphql.core.types.common import VendorError


from saleor.vendors import models
from saleor.graphql.core.mutations import (
    BaseMutation,
    ModelDeleteMutation,
    ModelMutation
)


class VendorCreateOrUpdate(ModelMutation):
    class Arguments:
        id = graphene.Argument(
            graphene.ID, description="ID of a Vendor to modify.", required=False
        )
        input = VendorCreateOrUpdateInput(
            description="Fields required to create a vendor.", required=True
        )

    # corregir:
    class Meta:
        description = "Creates a new vendor."
        permissions = ("is_superuser")
        # exclude = ["password"]
        model = models.Vendor
        error_type_class = VendorError
        error_type_field = "vendor_errors"

    @classmethod
    def mutate(cls, root, info, **data):
        response = super().mutate(root, info, **data)
        return response

    @classmethod
    def clean_input(cls, info, instance, data):
        return super().clean_input(info, instance, data)

    @classmethod
    @transaction.atomic
    def save(cls, info, instance, cleaned_input):
        instance.save()


class VendorImageCreate(BaseMutation):
    vendor = graphene.Field(Vendor)
    image = graphene.Field(VendorServiceImage)

    class Arguments:
        input = VendorImageCreateInput(
            description="Fields required to create a product image.")

    # corregir: permisos (solo servicios?) y ver errores
    class Meta:
        description = (
            "Create a vendor image."
        )
        permissions = ("is_superuser",)
        error_type_class = VendorError
        error_type_field = "vendor_errors"

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        data = data.get("input")
        vendor = cls.get_node_or_error(
            info, data["vendor"], field="vendor", only_type=Vendor
        )

        image_data = info.context.FILES.get(data["image"])
        validate_image_file(image_data, "image")

        if "position" in data.keys():
            image = vendor.service_images.create(
                image=image_data,
                alt=data.get("alt", ""),
                position=data.get("position"),
                title=data.get("title", "")
            )
        else:
            image = vendor.main_image.create(
                image=image_data,
                alt=data.get("alt", ""),
            )

        return ProductImageCreate(vendor=vendor, image=image)
