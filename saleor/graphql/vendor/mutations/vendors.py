import graphene
from graphql_relay import to_global_id
from django.db import transaction


from saleor.graphql.vendor.types.vendors import (
    Vendor,
    VendorLocation,
    VendorServiceImage,
    # VendorMainImage,
    VendorImageCreateOrUpdateInput,
    VendorCreateOrUpdateInput,
    VendorLocationCreateOrUpdateInput,
    VendorSocialMedia,
    VendorSocialMediaUpdateInput,
    VendorContact,
)
from saleor.graphql.core.utils import validate_image_file
from saleor.graphql.core.types.common import VendorError


from saleor.vendors import models
from saleor.product.models import Product as ProductModel
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


class VendorSocialMediaUpdate(BaseMutation):
    social_media = graphene.List(
        VendorSocialMedia, description="Social media of vendor.")

    class Arguments:
        social_media = graphene.List(
            VendorSocialMediaUpdateInput,
            description="list of IDs of base product services to modify.",
            required=True)

    # corregir: permisos
    class Meta:
        description = (
            "update social media of vendor."
        )
        error_type_class = VendorError
        error_type_field = "vendor_errors"

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        social_media_tuples = data.get("social_media")
        vendor_id = info.context.user.vendor_id
        vendor = models.Vendor.objects.get(id=vendor_id)

        updated = []

        for social_media in social_media_tuples:
            social_media_model, created = models.SocialMedia.objects.get_or_create(
                vendor=vendor, code=social_media["code"])
            social_media_model.user_string = social_media["user_string"]
            updated.append(VendorSocialMedia(
                code=social_media["code"], user_string=social_media["user_string"]))
            social_media_model.save()

        return VendorSocialMediaUpdate(social_media=updated)


class VendorServicesUpdate(BaseMutation):

    services = graphene.List(graphene.String, description="Services names.")

    class Arguments:
        services = graphene.List(
            graphene.ID, description="list of IDs of base product services to modify.", required=True)

    # corregir: permisos, borrar productos de servicios que no usa mas
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

        for service in vendor.services.all():
            services.append(service.name)
            product, created = ProductModel.objects.get_or_create(
                vendor=vendor,
                base_product=service,
                product_type=service.product_type,
                category=service.category
            )
            product.save()

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


class VendorImageCreateOrUpdate(BaseMutation):
    vendor = graphene.Field(Vendor)
    image_url = graphene.String(description="images' url")

    class Arguments:
        input = VendorImageCreateOrUpdateInput(
            description="Fields required to create a product image.")
        is_avatar = graphene.Boolean(required=False, description="Is avatar mutation.")

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
        input_data = data.get("input")
        vendor = cls.get_node_or_error(
            info, input_data["vendor_id"], field="vendor", only_type=Vendor
        )

        image_data = info.context.FILES.get(input_data["image"])
        validate_image_file(image_data, "image")

        if "position" in input_data.keys():
            image = vendor.service_images.filter(
                position=int(input_data['position'])).last()
            if not image:
                image = vendor.service_images.create(
                    position=int(input_data['position']))
            image.image = image_data
            image.title = input_data.get("title", "")

        elif data.get("is_avatar"):
            image = vendor.avatar_image.last()
            if not image:
                image = vendor.avatar_image.create(image=image_data)
            else:
                image.image = image_data

        else:
            image = vendor.main_image.last()
            if not image:
                image = vendor.main_image.create(image=image_data)
            else:
                image.image = image_data

        image.alt = input_data.get("alt", "")
        image.save()

        image_url = image.image.url

        return VendorImageCreateOrUpdate(vendor=vendor, image_url=image_url)
