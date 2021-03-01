# no se por que no funciona desde este archivo

# import graphene
# from django.db import transaction


# from saleor.vendors.models import Vendor
# from saleor.graphql.core.mutations import BaseMutation, ModelDeleteMutation, ModelMutation


# class VendorInput(graphene.InputObjectType):
#     description = graphene.String(description="Vendor description (HTML/text).")
#     name = graphene.String(description="Vendor name.")
#     slug = graphene.String(description="Vendor slug.")


# class VendorRegister(ModelMutation):
#     class Arguments:
#         input = VendorInput(
#             description="Fields required to create a vendor.", required=True
#         )

#     class Meta:
#         description = "Creates a new vendor."
#         # exclude = ["password"]
#         model = Vendor
#         # error_type_class = AccountError
#         # error_type_field = "account_errors"

#     @classmethod
#     def mutate(cls, root, info, **data):
#         response = super().mutate(root, info, **data)
#         return response

#     @classmethod
#     def clean_input(cls, info, instance, data):
#         return super().clean_input(info, instance, data)

#     @classmethod
#     @transaction.atomic
#     def save(cls, info, instance, cleaned_input):
#         instance.save()
