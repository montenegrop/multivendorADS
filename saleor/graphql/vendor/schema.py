import graphene
from graphene_federation import key
from graphene import relay
from saleor.vendors import models
from saleor.product.models import Category as CategoryModel
from saleor.graphql.core.types import Image
from saleor.graphql.core.types import ChannelSortInputObjectType

from saleor.graphql.utils import get_user_or_app_from_context


from saleor.graphql.meta.types import ObjectWithMetadata

from django.db import transaction

from saleor.graphql.channel.types import ChannelContextType, ChannelContextTypeWithMetadata


from graphene_django.types import DjangoObjectType, ObjectType

from saleor.vendors.models import Vendor as VendorModel
from saleor.graphql.core.mutations import BaseMutation, ModelDeleteMutation, ModelMutation

from saleor.graphql.channel import ChannelContext, ChannelQsContext

from saleor.graphql.core.fields import (
    ChannelContextFilterConnectionField,
    FilterInputConnectionField,
    PrefetchingConnectionField,
)

from saleor.graphql.core.connection import CountableDjangoObjectType


class VendorType(DjangoObjectType):
    class Meta:
        description = "Vendorszz"
        model = VendorModel


@key(fields="id")
class Vendor(ChannelContextTypeWithMetadata, CountableDjangoObjectType):

    main_image = graphene.Field(
        Image, size=graphene.Int(description="Size of the image.")
    )

    class Meta:
        default_resolver = ChannelContextType.resolver_with_context
        description = "Represents a vendor in the storefront."
        interfaces = [relay.Node, ObjectWithMetadata]
        model = VendorModel
        only_fields = [
            "description",
            "id",
            "name",
            "slug",
            "relevance",
        ]

    @staticmethod
    def resolve_main_image(root: VendorModel, info, size=None, **_kwargs):
        root = root.node
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


def resolve_vendors(
    info, requestor, channel_slug=None, **_kwargs
) -> ChannelQsContext:
    qs = models.Vendor.objects.all()
    return ChannelQsContext(qs=qs.distinct(), channel_slug=channel_slug)


class VendorSortField(graphene.Enum):
    NAME = ["name", "slug"]
    RELEVANCE = ["name", "relevance"]

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
    vendors = ChannelContextFilterConnectionField(
        Vendor,
        description="list all vendors",
        sort_by=VendorSortingInput(description="Sort categories."))
    # top_vendors = graphene.List(VendorType, description="list top ")
    # vendor = graphene.Field(
    #     Vendor,
    #     id=graphene.Argument(
    #         graphene.ID, description="ID of the vendor.", required=True),
    #     description="Look up a vendor by ID.",
    # )

    def resolve_vendors(self, info, channel=None, **kwargs):
        requestor = get_user_or_app_from_context(info.context)
        qs = VendorModel.objects.all()
        return resolve_vendors(info, requestor, channel_slug=channel, **kwargs)


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
