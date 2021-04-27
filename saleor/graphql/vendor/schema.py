import graphene
from graphene_federation import key
from graphene import relay
from saleor.vendors import models
from saleor.product.models import Category as CategoryModel
from saleor.graphql.core.types import Image
from saleor.graphql.core.types import ChannelSortInputObjectType

from saleor.graphql.utils import get_user_or_app_from_context

from saleor.graphql.vendor.dataloaders.vendors import ImagesByVendorIdLoader


from saleor.graphql.meta.types import ObjectWithMetadata

from django.db import transaction

from saleor.graphql.channel.types import ChannelContextType, ChannelContextTypeWithMetadata


from graphene_django.types import DjangoObjectType, ObjectType

from saleor.vendors.models import Vendor as VendorModel
from saleor.graphql.core.mutations import BaseMutation, ModelDeleteMutation, ModelMutation

from saleor.graphql.channel import ChannelContext, ChannelQsContext
from saleor.graphql.product.types import Category


from saleor.graphql.core.fields import (
    ChannelContextFilterConnectionField,
    FilterInputConnectionField,
    PrefetchingConnectionField,
)

from saleor.graphql.vendor.types.vendors import VendorImage, VendorContact


from saleor.graphql.core.connection import CountableDjangoObjectType


class VendorType(DjangoObjectType):
    class Meta:
        description = "Vendors"
        model = VendorModel


@key(fields="id")
class Vendor(CountableDjangoObjectType):

    main_image = graphene.Field(
        Image, size=graphene.Int(description="Size of the image."),
        description="Banner of the vendor"
    )

    images = graphene.List(
        lambda: VendorImage, description="List of images for the vendor."
    )

    main_categories = graphene.List(
        lambda: Category, description="List of level 0 categories used by the vendor."
    )

    contacts = graphene.List(
        lambda: VendorContact, description="List of contacts for the vendor."
    )

    class Meta:
        description = "Represents a vendor in the storefront."
        interfaces = [relay.Node, ObjectWithMetadata]
        model = VendorModel
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
        ]

    @staticmethod
    def resolve_main_image(root: VendorModel, info, size=None, **_kwargs):
        if root.main_image:
            return Image.get_adjusted(
                image=root.main_image,
                alt="vendor-alt-FALTA",
                size=size,
                rendition_key_set="main_images",
                info=info,
            )
        else:
            image = CategoryModel.objects.first().background_image
            return Image.get_adjusted(
                image=image,
                alt="vendor-alt-FALTA",
                size=size,
                rendition_key_set="main_images",
                info=info,
            )

    @staticmethod
    def resolve_images(root: VendorModel, info, **_kwargs):
        return ImagesByVendorIdLoader(info.context).load(root.id)

    @staticmethod
    def resolve_contacts(root: models.VendorContact, info, **_kwargs):
        return root.contacts.all()

    @staticmethod
    def resolve_main_categories(root: VendorModel, info, **_kwargs):
        categories = CategoryModel.objects.filter(
            products__vendor_id=root.id)
        return CategoryModel.objects.filter(
            children__in=categories).distinct().order_by(
            'relevance')


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


class VendorInput(graphene.InputObjectType):
    description = graphene.String(description="Vendor description (HTML/text).")
    name = graphene.String(description="Vendor name.")
    slug = graphene.String(description="Vendor slug.")


class VendorRegister(ModelMutation):
    class Arguments:
        input = VendorInput(
            description="Fields required to create a vendor.", required=True
        )

    class Meta:
        description = "Creates a new vendor."
        # exclude = ["password"]
        model = VendorModel
        # error_type_class = AccountError
        # error_type_field = "account_errors"

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


class VendorMutations(graphene.ObjectType):
    vendor_create = VendorRegister.Field()
