from ...core.connection import CountableDjangoObjectType
from ....service import models
import graphene
from graphene import relay
from graphene_federation import key


# class ServiceContract(CountableDjangoObjectType):

#     # corregir: objectwithmetadata
#     class Meta:
#         model = models.ServiceContract
#         # interfaces = [relay.Node]
#         only_fields = [
#             "id",
#         ]
#         interfaces = [relay.Node]


@key(fields="id")
class ServiceContractImage(CountableDjangoObjectType):
    url = graphene.String(
        required=True,
        description="The URL of the image.",
        size=graphene.Int(description="Size of the image."),
    )

    # corregir: ver si agregar otro campo en Meta
    class Meta:
        description = "Represents a service contract image."
        interfaces = [relay.Node]
        model = models.VendorContractReviewImage

    @staticmethod
    def resolve_url(root: models.VendorContractReviewImage, info, *, size=None):
        if size:
            url = get_thumbnail(root.image, size, method="thumbnail")
        else:
            url = root.image.url
        return info.context.build_absolute_uri(url)

    @staticmethod
    def __resolve_reference(root, _info, **_kwargs):
        return graphene.Node.get_node_from_global_id(_info, root.id)
