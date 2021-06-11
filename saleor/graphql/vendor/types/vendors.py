
import graphene
from graphene_federation import key
from graphene import relay
from graphene_django.types import DjangoObjectType, ObjectType

from saleor.graphql.core.fields import (
    FilterInputConnectionField,
)

from saleor.graphql.core.types import (
    Upload,
    Image,
    ChannelSortInputObjectType,
)

from saleor.graphql.meta.types import ObjectWithMetadata

from saleor.graphql.product.types import Category, PastExperience

from saleor.graphql.vendor.dataloaders.vendors import (
    ServiceImagesByVendorIdLoader,
)

from saleor.vendors import models
from saleor.account.models import User

from saleor.product.models import Category as CategoryModel
from saleor.product.models import PastExperience as PastExperienceModel


# from saleor.product.templatetags.product_images import get_thumbnail

from saleor.graphql.core.connection import CountableDjangoObjectType

# Campos de modelos para las queries:


@key(fields="id")
class VendorLocation(DjangoObjectType):

    class Meta:
        model = models.VendorLocation


@key(fields="id")
class VendorContact(DjangoObjectType):

    class Meta:
        model = models.VendorContact


class VendorSortField(graphene.Enum):
    NAME = ["name", "slug"]
    RELEVANCE = ["relevance", "name", "slug"]

    @property
    def description(self):
        # pylint: disable=no-member
        if self in [
            VendorSortField.NAME,
            VendorSortField.RELEVANCE,
        ]:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort categories by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)


class VendorSortingInput(ChannelSortInputObjectType):
    class Meta:
        sort_enum = VendorSortField
        type_name = "vendors"

# campos de tipos principales para las queries:


@key(fields="id")
class VendorServiceImage(CountableDjangoObjectType):
    url = graphene.String(
        description="The URL of the image.",
        size=graphene.Int(description="Size of the image."),
    )

    class Meta:
        description = "Represents a vendor image."
        only_fields = ["alt", "id", "sort_order", "title", "position"]
        interfaces = [relay.Node]
        model = models.VendorServiceImage

    @staticmethod
    def resolve_url(root: models.VendorServiceImage, info, *, size=None):
        if size:
            pass
            # url = get_thumbnail(root.image, size, method="thumbnail")
        else:
            url = root.image.url
        return info.context.build_absolute_uri(url)

    # @staticmethod
    # def __resolve_reference(root, _info, **_kwargs):
    #     return graphene.Node.get_node_from_global_id(_info, root.id)


@key(fields="id")
class VendorMainImage(DjangoObjectType):
    url = graphene.String(
        description="The URL of the image.",
        size=graphene.Int(description="Size of the image."),
    )

    class Meta:
        description = "Represents a vendor main image."
        only_fields = ["alt", "id"]
        interfaces = [relay.Node]
        model = models.VendorMainImage

    @staticmethod
    def resolve_url(root: models.VendorMainImage, info, *, size=None):
        if size:
            pass
            # url = get_thumbnail(root.image, size, method="thumbnail")
        else:
            url = root.image.url
        return info.context.build_absolute_uri(url)


@key(fields="id")
class ServiceContact(ObjectType):

    first_name = graphene.String(description="Name and last name.")
    last_name = graphene.String(description="Name and last name.")
    full_name = graphene.String(description="Full name.")
    phone = graphene.String(description="Phone: might not be cellphone.")
    celphone = graphene.String(description="Cellphone.")
    city = graphene.String(description="City.")
    postal_code = graphene.String(description="Postal code.")
    city_with_code = graphene.String(
        description="City with postal code, ex: Rosario(2000).")
    address = graphene.String(description="Address: Street and postal code.")
    email = graphene.String(description="Email.")
    # social_media = graphene.List(SocialMedia, description="Social media information.")

    # @staticmethod
    # def resolve_social_media(root, info, **_kwargs):
    #     ''' load toma tambien la variable last '''
    #     return root.full_name

    @staticmethod
    def resolve_full_name(root, info, **_kwargs):
        return root.first_name + root.last_name

    @staticmethod
    def resolve_city_with_code(root, info, **_kwargs):
        return f'{root.city} ({root.postal_code})'


@key(fields="id")
class Vendor(CountableDjangoObjectType):

    service_contact = graphene.Field(
        ServiceContact, description="Contact fields for service providers.")

    past_experiences = FilterInputConnectionField(
        PastExperience, description="Past experiences when vendor gives services.")

    main_image = graphene.Field(VendorMainImage, description="Vendor main image.")

    service_images = graphene.List(
        lambda: VendorServiceImage, description="List of service images for the vendor."
    )

    main_categories = graphene.List(
        lambda: Category, description="List of level 0 categories used by the vendor."
    )

    class Meta:
        description = "Represents a vendor in the storefront."
        interfaces = [relay.Node, ObjectWithMetadata]
        model = models.Vendor
        only_fields = [
            "id",
            "name",
            "slug",
            "relevance",
            "description",
            "bussiness",
            "founding_year",
            "total_employess",
            "quality_norms",
            "open_hours",
            "billing",
            "website_url",
            "phone",
            "address",
            "email",
            "location",
            "contacts",
            "services",
        ]

    @staticmethod
    def resolve_service_contact(root: models.Vendor, info, **_kwargs):
        # corregir: user with vendor first()
        user_of_vendor = User.objects.filter(vendor=root).first()
        first_name = user_of_vendor.first_name
        last_name = user_of_vendor.last_name
        email = user_of_vendor.email
        phone = user_of_vendor.phone
        location = root.location
        # address = location.full_address
        city = location.city
        postal_code = location.postal_code

        return ServiceContact(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            city=city,
            postal_code=postal_code
        )

    # corregir: (formato imagen banner, ver get_adjusted)
    @staticmethod
    def resolve_main_image(root: models.Vendor, info, size=None, **_kwargs):
        if root.main_image:
            return models.VendorMainImage.objects.filter(vendor_id=root.id).last()

        # if root.main_image:
        #     return Image.get_adjusted(
        #         image=root.main_image.first(),
        #         alt="vendor-alt-FALTA",
        #         size=size,
        #         rendition_key_set="main_images",
        #         info=info,
        #     )

    @staticmethod
    def resolve_service_images(root: models.Vendor, info, **_kwargs):
        ''' load toma tambien la variable last '''
        return ServiceImagesByVendorIdLoader(info.context).load(root.id)

    @staticmethod
    def resolve_main_categories(root: models.Vendor, info, **_kwargs):
        categories = CategoryModel.objects.filter(
            products__vendor_id=root.id)
        return CategoryModel.objects.filter(
            children__in=categories).distinct().order_by(
            'relevance')

    @staticmethod
    def resolve_past_experiences(root: models.Vendor, info, **_kwargs):
        return PastExperienceModel.objects.exclude(description_short__isnull=True)
        # return PastExperiencesByVendorIdLoader(info.context).load(root.id)


# Input para mutaciones:


class VendorCreateOrUpdateInput(graphene.InputObjectType):
    # corregir: (no modificable por usuario)
    slug = graphene.String(description="Vendor slug. Is unicode", required=False)

    # basicos:
    name = graphene.String(description="Vendor name.", required=False)
    description = graphene.String(
        description="Vendor description (HTML/text).", required=False)


class VendorImageCreateInput(graphene.InputObjectType):
    vendor_id = graphene.ID(required=True, description="ID of a vendor.")
    image = Upload(required=True, description="Image file.")
    title = graphene.String(required=False, description="Image title.")
    position = graphene.String(required=False, description="Image position.")
    alt = graphene.String(required=False, description="Alt text for an image.")


class VendorLocationCreateOrUpdateInput(graphene.InputObjectType):
    province = graphene.String(description="Vendor province.", required=False)
    city = graphene.String(description="Vendor city.", required=False)
    postal_code = graphene.String(description="Vendor postal code.", required=False)
    lat = graphene.String(description="Vendor lat.", required=False)
    lon = graphene.String(description="Vendor lon.", required=False)
