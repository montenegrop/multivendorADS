
import graphene
from graphene_federation import key
from graphene import relay
from graphene_django.types import DjangoObjectType

from saleor.graphql.core.types import (
    Upload,
    Image,
    ChannelSortInputObjectType,
)

from saleor.graphql.meta.types import ObjectWithMetadata

from saleor.graphql.product.types import Category

from saleor.graphql.vendor.dataloaders.vendors import ImagesByVendorIdLoader

from saleor.vendors import models

from saleor.product.models import Category as CategoryModel


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
class Vendor(CountableDjangoObjectType):

    main_image = graphene.Field(
        VendorMainImage, size=graphene.Int(description="Size of the image."),
        description="Banner of the vendor"
    )

    service_images = graphene.List(
        lambda: VendorServiceImage, description="List of images for the vendor."
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
        ]

    # corregir: (formato imagen banner)
    @staticmethod
    def resolve_main_image(root: models.Vendor, info, size=None, **_kwargs):
        return ImagesByVendorIdLoader(info.context).load(root.id)

        # if root.main_image:
        #     return Image.get_adjusted(
        #         image=root.main_image.image,
        #         alt="vendor-alt-FALTA",
        #         size=size,
        #         rendition_key_set="main_images",
        #         info=info,
        #     )

    # load toma tambien la variable 'last':
    @staticmethod
    def resolve_service_images(root: models.Vendor, info, **_kwargs):
        return ImagesByVendorIdLoader(info.context).load(root.id)

    @staticmethod
    def resolve_main_categories(root: models.Vendor, info, **_kwargs):
        categories = CategoryModel.objects.filter(
            products__vendor_id=root.id)
        return CategoryModel.objects.filter(
            children__in=categories).distinct().order_by(
            'relevance')

# Input para mutaciones:


class VendorCreateOrUpdateInput(graphene.InputObjectType):
    # corregir: (no modificable por usuario)
    slug = graphene.String(description="Vendor slug. Is unicode", required=False)

    # basicos:
    name = graphene.String(description="Vendor name.", required=False)
    description = graphene.String(
        description="Vendor description (HTML/text).", required=False)


class VendorImageCreateInput(graphene.InputObjectType):
    vendor = graphene.ID(
        required=True, description="ID of a vendor.", name="vendor"
    )
    image = Upload(required=True, description="Image file.")
    title = graphene.String(required=False, description="Image title.")
    position = graphene.String(required=False, description="Image position.")
    alt = graphene.String(required=False, description="Alt text for an image.")
