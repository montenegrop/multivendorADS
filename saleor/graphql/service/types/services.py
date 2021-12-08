from ...core.connection import CountableDjangoObjectType
from ...service import models


class PastExperience(CountableDjangoObjectType):

    service = graphene.Field(BaseProduct)

    # corregir: objectwithmetadata
    class Meta:
        model = models.PastExperience
        # interfaces = [relay.Node]
        only_fields = [
            "id",
            "year_performed",
            "description_short",
            "description_long",
            "past_experience_images",
            "location",
        ]
        interfaces = [relay.Node, ObjectWithMetadata]

    @staticmethod
    def resolve_service(root: models.PastExperience, info):
        return root.product.base_product
