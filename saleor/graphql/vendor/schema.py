import graphene
from django.db import transaction

from graphene_django.types import DjangoObjectType, ObjectType

from saleor.vendors.models import Vendor
from saleor.graphql.core.mutations import BaseMutation, ModelDeleteMutation, ModelMutation


class VendorType(DjangoObjectType):
    class Meta:
        description = "Vendors"
        model = Vendor


class VendorQueries(graphene.ObjectType):
    vendors = graphene.List(VendorType, description="list all vendors")
    # vendor = graphene.Field(
    #     Vendor,
    #     id=graphene.Argument(
    #         graphene.ID, description="ID of the vendor.", required=True),
    #     description="Look up a vendor by ID.",
    # )

    def resolve_vendors(self, info, **kwargs):
        return Vendor.objects.all()

    # def resolve_vendor(self, info, id):
    #     return Vendor.object.get(id=id)


class VendorInput(graphene.InputObjectType):
    description = graphene.String(description="Vendor description (HTML/text).")
    name = graphene.String(description="Vendor name.")
    slug = graphene.String(description="Vendor slug.")
    pk = graphene.ID(description="ID of the vendor.")


class VendorRegister(ModelMutation):
    class Arguments:
        input = VendorInput(
            description="Fields required to create a vendor.", required=True
        )

    class Meta:
        description = "Creates a new vendor."
        # exclude = ["password"]
        model = Vendor
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

    # @classmethod
    # def get_form_kwargs(cls, root, info, **input):
    #     kwargs = {"data": input}

    #     global_id = input.pop("id", None)
    #     if global_id:
    #         node_type, pk = from_global_id(global_id)
    #         instance = cls._meta.model._default_manager.get(pk=pk)
    #         kwargs["instance"] = instance
    #     return kwargs


class VendorMutations(graphene.ObjectType):
    vendor_create = VendorRegister.Field()
