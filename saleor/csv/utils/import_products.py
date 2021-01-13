from django.db import models
from django.db.models.fields import BooleanField, IntegerField, CharField
from django.http import HttpResponse, HttpResponseBadRequest
from django.db.models.fields.related import ManyToManyField, ForeignKey

from openpyxl import load_workbook
from saleor.product.models import Product, ProductVariant, ProductType


# variant_readed_attributes:
VARIANT_SKU = "variant sku"


product_readed_attributes = {
    "name": "name",
    # "category": "category",
    "product type": "product_type",
}


def row_to_object(headers, data, vendor_id):

    sku_simple = None
    for i, header in enumerate(headers):
        sku_simple = data[i] if header == VARIANT_SKU else sku_simple

    if ProductVariant.objects.filter(
            sku_simple=sku_simple, product__vendor_id=vendor_id).exists():
        product_variant = ProductVariant.objects.filter(
            sku_simple=sku_simple, product__vendor_id=vendor_id).first()
    else:
        sku = sku_simple + '00000' + str(vendor_id)
        product_variant = ProductVariant(sku=sku, sku_simple=sku_simple)

    product = product_variant.product if product_variant.product_id else Product()

    for n, attr_name in enumerate(headers):
        value = data[n]
        # change read attr_name from ImportedProductAttributes to product real attribute:
        try:
            attr_name = product_readed_attributes[attr_name]
            if attr_name == "name":
                product.__setattr__(attr_name, value)
            if attr_name == "product_type":
                print('here')
                product_type = ProductType.objects.get(name=value)
                # product_type.slug = "slug_type" + str(n)
                product.product_type = product_type
        except KeyError:
            continue
        else:
            print("unexpected error")
    product.save()
    product_variant.product = product
    product_variant.save()

    return


def verify_products_from_xlsx(filename):
    try:
        wb = load_workbook(filename=filename)
    except:
        return (False, "fail reason")

    return (True, "no errors")


def import_products_from_xlsx(filename, vendor_id):
    verify_products_from_xlsx(filename=filename)
    wb = load_workbook(filename=filename)
    ws = wb.active

    headers = []
    for n, row in enumerate(ws.iter_rows()):
        data = []
        for cell in row:
            headers.append(cell.value) if n == 0 else data.append(cell.value)

        if len(data):
            row_to_object(headers, data, vendor_id)
        try:
            pass
        except Exception as e:
            raise e
            return HttpResponseBadRequest(str(e))
    return HttpResponse('File imported successfully')
