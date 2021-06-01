import graphene
from graphql_relay import to_global_id
from django.db import transaction


from saleor.graphql.vendor.types.vendors import (
    Vendor,
    VendorLocation,
    VendorServiceImage,
    # VendorMainImage,
    VendorImageCreateInput,
    VendorCreateOrUpdateInput,
    VendorLocationCreateOrUpdateInput,
)
from saleor.graphql.core.utils import validate_image_file
from saleor.graphql.core.types.common import VendorError


from saleor.vendors import models
from saleor.graphql.core.mutations import (
    BaseMutation,
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


class VendorServicesUpdate(BaseMutation):

    services = graphene.List(graphene.String, description="Services names.")

    class Arguments:
        services = graphene.List(
            graphene.ID, description="list of IDs of base product services to modify.", required=True)

    # corregir: permisos
    class Meta:
        description = (
            "update services provided by vendor."
        )
        error_type_class = VendorError
        error_type_field = "vendor_errors"

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        services_global_ids = data.get("services")
        vendor_id = info.context.user.vendor_id
        vendor = models.Vendor.objects.get(id=vendor_id)

        ids_of_services = []
        [ids_of_services.append(graphene.Node.from_global_id(service_global_id)[
                                1]) for service_global_id in services_global_ids]

        # borrar servicios que no provee más:
        services_to_be_removed = vendor.services.exclude(id__in=ids_of_services)
        vendor.services.remove(*services_to_be_removed)

        # agregar servicios nuevos:
        vendor.services.add(*ids_of_services)

        services = []
        [services.append(service.name) for service in vendor.services.all()]

        return VendorServicesUpdate(services=services)


class VendorLocationCreateOrUpdate(ModelMutation):
    class Arguments:
        id = graphene.Argument(
            graphene.ID, description="ID of a Vendor to modify.", required=False
        )
        input = VendorLocationCreateOrUpdateInput(
            description="Fields required to modify vendor location.", required=True
        )

    # corregir:
    class Meta:
        description = "Modify vendor location."
        permissions = ("is_superuser")
        # exclude = ["password"]
        model = models.VendorLocation
        error_type_class = VendorError
        error_type_field = "vendor_errors"

    @ classmethod
    def mutate(cls, root, info, **data):
        vendor = info.context.user.vendor
        if 'id' not in data.keys() and vendor.location:
            vendor_location_global_id = to_global_id(
                VendorLocation._meta.name, vendor.location.pk)
            data['id'] = vendor_location_global_id

        response = super().mutate(root, info, **data)
        return response

    @ classmethod
    def clean_input(cls, info, instance, data):
        return super().clean_input(info, instance, data)

    @ classmethod
    @ transaction.atomic
    def save(cls, info, instance, cleaned_input):
        instance.save()
        if not info.context.user.vendor.location:
            info.context.user.vendor.location = instance
            info.context.user.vendor.save()


class VendorImageCreate(BaseMutation):
    vendor = graphene.Field(Vendor)
    image_url = graphene.String(description="images' url")

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
            info, data["vendor_id"], field="vendor", only_type=Vendor
        )

        image_data = info.context.FILES.get(data["image"])
        validate_image_file(image_data, "image")

        if "position" in data.keys():

            image = vendor.service_images.filter(position=int(data['position'])).last()
            if not image:
                image = vendor.service_images.create(position=int(data['position']))
            image.image = image_data
            image.title = data.get("title", "")

        else:
            image = vendor.main_image.last()
            if not image:
                image = vendor.main_image.create(image=image_data)
            else:
                image.image = image_data

        image.alt = data.get("alt", "")
        image.save()

        image_url = image.image.url

        return VendorImageCreate(vendor=vendor, image_url=image_url)
