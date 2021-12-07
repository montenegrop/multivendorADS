from datetime import datetime, timezone, timedelta

import graphene

from saleor.graphql.core.mutations import BaseMutation

from saleor.service.models import ServiceContract
from saleor.account.models import User
from saleor.vendors.models import Vendor
from saleor.product.models import BaseProduct
from saleor.graphql.utils import get_database_id

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
        contract_id = graphene.relay.Node.to_global_id('BaseProduct', int(contract.id))
        return ServiceContractCreateOrUpdate(error='', contract_id=contract_id)


class ServiceMutations(graphene.ObjectType):
    service_contract_create_or_update = ServiceContractCreateOrUpdate.Field()
