
import graphene
from graphene_federation import key
from graphene import relay
from graphene_django.types import DjangoObjectType
from saleor.vendors import models
from saleor.graphql.core.types import Upload

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


class VendorImageCreateInput(graphene.InputObjectType):
    vendor = graphene.ID(
        required=True, description="ID of a vendor.", name="vendor"
    )
    image = Upload(required=True, description="Image file.")
    title = graphene.String(required=False, description="Image title.")
    position = graphene.String(required=False, description="Image position.")
    alt = graphene.String(required=False, description="Alt text for an image.")


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
        model = models.VendorServiceImage

    @staticmethod
    def resolve_url(root: models.VendorServiceImage, info, *, size=None):
        if size:
            pass
            # url = get_thumbnail(root.image, size, method="thumbnail")
        else:
            url = root.image.url
        return info.context.build_absolute_uri(url)

    @staticmethod
    def __resolve_reference(root, _info, **_kwargs):
        return graphene.Node.get_node_from_global_id(_info, root.id)
