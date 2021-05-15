
import graphene
from graphene_federation import key
from graphene import relay
from graphene_django.types import DjangoObjectType
from saleor.vendors import models

# from saleor.product.templatetags.product_images import get_thumbnail

from saleor.graphql.core.connection import CountableDjangoObjectType


@key(fields="id")
class VendorLocation(DjangoObjectType):

    class Meta:
        model = models.VendorLocation


@key(fields="id")
class VendorContact(DjangoObjectType):

    class Meta:
        model = models.VendorContact


@key(fields="id")
class VendorImage(CountableDjangoObjectType):
    url = graphene.String(
        required=True,
        description="The URL of the image.",
        size=graphene.Int(description="Size of the image."),
    )

    class Meta:
        description = "Represents a vendor image."
        only_fields = ["alt", "id", "sort_order", "title", "position"]
        interfaces = [relay.Node]
        model = models.VendorImage

    @staticmethod
    def resolve_url(root: models.VendorImage, info, *, size=None):
        if size:
            pass
            # url = get_thumbnail(root.image, size, method="thumbnail")
        else:
            url = root.image.url
        return info.context.build_absolute_uri(url)

    @staticmethod
    def __resolve_reference(root, _info, **_kwargs):
        return graphene.Node.get_node_from_global_id(_info, root.id)
