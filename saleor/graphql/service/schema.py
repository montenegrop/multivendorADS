from datetime import datetime, timezone, timedelta

import graphene

from saleor.graphql.core.mutations import BaseMutation

from saleor.service.models import ServiceContract as ServiceContractModel
from saleor.account.models import User
from saleor.vendors.models import Vendor
from saleor.product.models import BaseProduct
from saleor.graphql.utils import get_database_id

from ..core.types import Upload
from ..core.types.common import ProductError

from .types import (
    ServiceContractImage,
)

from saleor.graphql.vendor.types.vendors import ServiceContract

# corregir constants:
# zona = timezone(timedelta(hours=-3), name="argentina-3")
# tiempo = datetime(year=int(date_array[0]), month=int(date_array[1]), day=int(date_array[2]), hour=int(hour_array[0]),
#                               minute=int(hour_array[1]), tzinfo=zona)


class ServiceContractCreateOrUpdateInput(graphene.InputObjectType):
    date = graphene.String(required=True)
    hour = graphene.String(required=True)
    city = graphene.String(required=True)
    address = graphene.String(required=True)
    message = graphene.String(required=True)
    stage = graphene.String(required=True)


class ServiceContractCreateOrUpdate(BaseMutation):
    error = graphene.String()
    contract_id = graphene.String()

    class Arguments:
        id = graphene.ID(description="ID of the Contract.")
        creating = graphene.Boolean(required=False)
        vendor_id = graphene.String(
            description="Vendor id of service provider.", required=False)
        service_id = graphene.String(
            description="Service id requested.", required=False)
        accepting = graphene.Boolean()
        concreted = graphene.Boolean()
        service_reviewing = graphene.Boolean()
        user_reviewing = graphene.Boolean()
        input = ServiceContractCreateOrUpdateInput(
            description="Fields required to create a vendor.", required=True
        )
    # corregir: permisos

    class Meta:
        description = (
            "creates or updates contract between user and service provider (vendor)."
        )
        error_type_field = "service_errors"

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        if data['creating']:
            stage = 1

            date_array = data['input']['date'].split("-")
            hour_array = data['input']['hour'].split(":")

            address = data['input']['address']
            city = data['input']['city']
            message = data['input']['message']

            tiempo = datetime(year=int(date_array[0]), month=int(date_array[1]), day=int(date_array[2]), hour=int(hour_array[0]),
                              minute=int(hour_array[1]))

            user = info.context.user
            if 'vendor_if' in data.keys():
                vendor = Vendor.objects.get(id=int(data['vendor_id']))
            else:
                vendor = Vendor.objects.get(id=3)

            service_db_id = get_database_id(info='info', only_type='BaseProduct',
                                            node_id=data['service_id'])
            service = BaseProduct.objects.get(id=service_db_id)
            contract = ServiceContract(
                user=user, vendor=vendor, date=tiempo, address=address, localidad=city, message=message, service=service)
        else:
            user = User.objects.get(id=3)

        contract.save()
        contract_id = graphene.relay.Node.to_global_id(
            'ServiceContract', int(contract.id))
        return ServiceContractCreateOrUpdate(error='', contract_id=contract_id)


class ServiceContractCreateInput(graphene.InputObjectType):
    alt = graphene.String(description="Alt text for an image.")
    position = graphene.String(
        required=True, description="Values from 0 to 4. 0 is main service contract image.")
    image = Upload(
        required=True, description="Represents an image file in a multipart request."
    )
    service_contract = graphene.ID(
        required=True, description="ID of a service contract."
    )


class ServiceContractImageCreate(BaseMutation):
    service_contract = graphene.Field(ServiceContract)
    image = graphene.Field(ServiceContractImage)
    position = graphene.String(description="Position of image.")

    class Arguments:
        input = ServiceContractCreateInput(
            required=True, description="Fields required to create a service contract image."
        )

    # corregir: ver permisos
    class Meta:
        description = (
            "Create a service contrawct image. This mutation must be sent as a `multipartt` "
            "request."
        )
        permissions = ("is_superuser")
        error_type_class = ProductError
        error_type_field = "product_errors"

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        data = data.get("input")
        service_contract = cls.get_node_or_error(
            info=info, node_id=data["service_contract"], only_type=ServiceContract)

        image_data = info.context.FILES.get(data["image"])
        # validate_image_file(image_data, "image")

        image, created = service_contract.vendor_contract_review_images.update_or_create(
            image=image_data, alt=data.get("alt", ""), position=int(data["position"]))
        return PastExperienceImageCreate(
            service_contract=service_contract,
            image=image,
            position=image.position
        )


class ServiceMutations(graphene.ObjectType):
    service_contract_create_or_update = ServiceContractCreateOrUpdate.Field()
    service_contract_image_create = ServiceContractImageCreate.Field()
