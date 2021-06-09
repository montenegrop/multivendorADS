import logging

from saleor import settings

from django.core.management.base import BaseCommand
from tqdm import tqdm

from saleor.product.models import BaseProduct, Category, ProductType

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Creates BaseProduct for each subcategory of the category" + \
        "'services' with the same name as the subcategory and in that same subcategory."

    def handle(self, *args, **options):
        self.stdout.write('Updating base_services derived form service subcategories.')
        # Fetching the discounts just once and reusing them
        # Run the update on all the products with "progress bar" (tqdm)

        print('ada')

        service_product_type = ProductType.objects.get(
            name=settings.NAME_OF_SERVICES_PRODUCT_TYPE)

        print(service_product_type.name)

        service_subcategories = Category.objects.filter(
            parent__name=settings.NAME_OF_SERVICES_CATEGORY)

        print(service_subcategories)

        [print(service_subcategorie.name)
         for service_subcategorie in service_subcategories]

        for service_subcategory in service_subcategories:
            new_product, created = BaseProduct.objects.get_or_create(
                name=service_subcategory.name,
            )
            print(new_product.name, created)
            service_subcategory.category = service_subcategory
            service_subcategory.product_type = service_product_type
            service_subcategory.save()
