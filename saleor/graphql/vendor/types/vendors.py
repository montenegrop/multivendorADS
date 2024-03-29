
import graphene
from graphene_federation import key
from graphene import relay
from graphene.relay import is_node
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
from saleor.service.models import ServiceContract as ServiceContractModel
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
class VendorAvatarImage(DjangoObjectType):
    url = graphene.String(
        description="The URL of the avatar image.",
        size=graphene.Int(description="Size of the image."),
    )

    class Meta:
        description = "Represents the vendor's avatar image."
        only_fields = ["alt", "id"]
        interfaces = [relay.Node]
        model = models.VendorAvatarImage

    @staticmethod
    def resolve_url(root: models.VendorAvatarImage, info, *, size=None):
        if size:
            pass
            # url = get_thumbnail(root.image, size, method="thumbnail")
        else:
            url = root.image.url
        return info.context.build_absolute_uri(url)


@key(fields="id")
class VendorMainImage(DjangoObjectType):
    url = graphene.String(
        description="The URL of the main image.",
        size=graphene.Int(description="Size of the image."),
    )

    class Meta:
        description = "Represent the vendor's main image."
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
class VendorSocialMedia(ObjectType):
    code = graphene.String(description="Social media code.")
    user_string = graphene.String(description="Social media user, not url.")
    url = graphene.String(description="Full social media url of vendor.")

    # @staticmethod
    # def resolve_code(root, info, **_kwargs):
    #     return "IG"

    # @staticmethod
    # def resolve_user(root, info, **_kwargs):
    #     return "marizzadenoche"

    @staticmethod
    def resolve_url(root, info, **_kwargs):
        return "https://www.xd.com/" + root.code


@key(fields="id")
class ServiceContract(CountableDjangoObjectType):
    first_name = graphene.String(description="Name.")
    last_name = graphene.String(description="Last name.")
    full_name = graphene.String(description="Full name.")
    phone = graphene.String(description="Phone: might not be cellphone.")
    cellphone = graphene.String(description="Cellphone.")
    city = graphene.String(description="City.")
    postal_code = graphene.String(description="Postal code.")
    city_with_code = graphene.String(
        description="City with postal code, ex: Rosario(2000).")
    address = graphene.String(description="Address: Street and postal code.")
    email = graphene.String(description="Email.")
    datetime = graphene.String(description="date and time of service.")
    service = graphene.String(description="Nombre del servicio.")
    # social_media = graphene.List(SocialMedia, description="Social media information.")

    class Meta:
        model = ServiceContractModel
        # interfaces = [relay.Node]
        only_fields = [
            "id",
            "address",
            "message",
        ]
        interfaces = [relay.Node, ObjectWithMetadata]

    # @staticmethod
    # def resolve_social_media(root, info, **_kwargs):
    #     ''' load toma tambien la variable last '''
    #     return root.full_name

    @staticmethod
    def resolve_datetime(root, info, **_kwargs):
        return root.datetime

    @staticmethod
    def resolve_city(root, info, **_kwargs):
        return root.localidad

    @staticmethod
    def resolve_service(root, info, **_kwargs):
        return root.service.name

    @staticmethod
    def resolve_email(root, info, **_kwargs):
        return root.user.email

    @staticmethod
    def resolve_phone(root, info, **_kwargs):
        return root.user.phone

    @staticmethod
    def resolve_cellphone(root, info, **_kwargs):
        return root.user.cellphone

    @staticmethod
    def resolve_first_name(root, info, **_kwargs):
        return root.user.first_name

    @staticmethod
    def resolve_last_name(root, info, **_kwargs):
        return root.user.last_name

    @staticmethod
    def resolve_full_name(root, info, **_kwargs):
        return root.user.first_name + root.user.last_name

    @staticmethod
    def resolve_city_with_code(root, info, **_kwargs):
        if root.city:
            return f'{root.city} ({root.postal_code})'
        else:
            return ""


@key(fields="id")
class Vendor(CountableDjangoObjectType):

    service_contracts = FilterInputConnectionField(
        ServiceContract, description="Contact fields for service providers.")

    past_experiences = FilterInputConnectionField(
        PastExperience, description="Past experiences when vendor gives services.")

    main_image = graphene.Field(VendorMainImage, description="Vendor main image.")

    avatar_image = graphene.Field(VendorAvatarImage, description="Vendor main image.")

    service_images = graphene.List(
        lambda: VendorServiceImage, description="List of service images for the vendor."
    )

    main_categories = graphene.List(
        lambda: Category, description="List of level 0 categories used by the vendor."
    )

    category = graphene.Field(Category, id=graphene.Argument(
        graphene.ID, description="ID of the category."), description="To filter by a single category.")

    social_media = graphene.List(VendorSocialMedia, description="Vendor social media.")

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
    def resolve_social_media(root: models.Vendor, info, **_kwargs):
        social_media_list = []
        for social_media in root.social_media.all():
            social_media_list.append(VendorSocialMedia(
                code=social_media.code, user_string=social_media.user_string))
        return social_media_list

    @staticmethod
    def resolve_service_contracts(root: models.Vendor, info, **_kwargs):
        # corregir: user with vendor first()
        user_of_vendor = User.objects.filter(vendor=root).first()
        contracts = ServiceContractModel.objects.filter(vendor=root)
        return contracts

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
    def resolve_avatar_image(root: models.Vendor, info, size=None, **_kwargs):
        if root.avatar_image:
            return models.VendorAvatarImage.objects.filter(vendor_id=root.id).last()

    # corregir:
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
    def resolve_category(root: models.Vendor, info, **_kwargs):
        category = CategoryModel.objects.filter(
            products__vendor_id=root.id)
        return CategoryModel.objects.filter(
            children__in=category)

    @staticmethod
    def resolve_past_experiences(root: models.Vendor, info, **_kwargs):
        return PastExperienceModel.objects.exclude(
            product__isnull=True,
        )
        # return PastExperiencesByVendorIdLoader(info.context).load(root.id)


# Input para mutaciones:


class VendorCreateOrUpdateInput(graphene.InputObjectType):
    # corregir: (no modificable por usuario)
    slug = graphene.String(description="Vendor slug. Is unicode", required=False)

    # basicos:
    name = graphene.String(description="Vendor name.", required=False)
    description = graphene.String(
        description="Vendor description (HTML/text).", required=False)


class VendorContactUpdateInput(graphene.InputObjectType):
    vendor_id = graphene.ID(required=True, description="ID of a vendor.")


class VendorImageCreateOrUpdateInput(graphene.InputObjectType):
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


class VendorSocialMediaUpdateInput(graphene.InputObjectType):
    code = graphene.String(description="Social media code", required=True)
    user_string = graphene.String(description="Social media username.", required=False)
