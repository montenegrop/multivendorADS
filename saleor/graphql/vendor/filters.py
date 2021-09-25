import django_filters

from graphene_django.filter import GlobalIDMultipleChoiceFilter


from ...vendors.models import Vendor
from ...product.models import BaseProduct
from ..utils import get_nodes


def filter_vendors_by_services(qs, _, services):
    if services:
        services = get_nodes(services, "BaseProduct", BaseProduct)
        return qs.filter(services__in=services)
    return qs


class VendorFilter(django_filters.FilterSet):
    services = GlobalIDMultipleChoiceFilter(method=filter_vendors_by_services)

    class Meta:
        model = Vendor
        fields = [
            "services",
        ]
