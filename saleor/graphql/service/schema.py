from datetime import datetime, timezone, timedelta

import graphene

from saleor.graphql.core.mutations import BaseMutation

from saleor.service.models import ServiceContract
from saleor.account.models import User
from saleor.vendors.models import Vendor
from saleor.product.models import BaseProduct
from saleor.graphql.utils import get_database_id


class ServiceContractCreateOrUpdateInput(graphene.InputObjectType):
    date = graphene.String(required=True)
    address = graphene.String(required=True)
    message = graphene.String(required=True)
    stage = graphene.String(required=True)


class ServiceContractCreateOrUpdate(BaseMutation):
    error = graphene.String()
    contract_id = graphene.String()

    class Arguments:
        id = graphene.ID(description="ID of the Contract.")
        creating = graphene.Boolean()
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

            zona = timezone(timedelta(hours=-3), name="argentina-3")
            tiempo = datetime(year=2019, month=6, day=27, hour=3,
                              minute=0, second=0, tzinfo=zona)
            tiempo2 = datetime.strptime("March 5, 2014, 20:13:50", "%B %d, %Y, %H:%M:%S").replace(
                tzinfo=timezone(timedelta(hours=-8), name="menos8"))
            user = info.context.user
            if 'vendor_if' in data.keys():
                vendor = Vendor.objects.get(id=int(data['vendor_id']))
            else:
                vendor = Vendor.objects.get(id=3)

            service_db_id = get_database_id(info='info', only_type='BaseProduct',
                                            node_id=data['service_id'])
            service = BaseProduct.objects.get(id=service_db_id)
            contract = ServiceContract(
                user=user, vendor=vendor, date=tiempo, service=service)
        else:
            user = User.objects.get(id=3)

        contract.save()
        contract_id = graphene.relay.Node.to_global_id('BaseProduct', int(contract.id))
        return ServiceContractCreateOrUpdate(error='', contract_id=contract_id)


class ServiceMutations(graphene.ObjectType):
    service_contract_create_or_update = ServiceContractCreateOrUpdate.Field()
