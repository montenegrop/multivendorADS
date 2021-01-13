from django.db import models
from django.db.models.fields import BooleanField, IntegerField, CharField
from django.http import HttpResponse, HttpResponseBadRequest
from django.db.models.fields.related import ManyToManyField, ForeignKey

from openpyxl import load_workbook
from saleor.product.models import Product, ProductVariant, ProductType, Vendor


# variant attributes:
VARIANT_SKU = {"header": "variant sku", "attribute": "sku_simple"}

# products attributes:
PRODUCT_ID = {"header": "id", "attribute": "id_simple"}
PRODUCT_NAME = {"header": "name", "attribute": "name"}
PRODUCT_TYPE_NAME = {"header": "product type", "attribute": "product_type"}


def row_to_object(headers, data, vendor_id):

    sku_simple = None
    id_simple = None
    for i, header in enumerate(headers):
        sku_simple = data[i] if header == VARIANT_SKU['header'] else sku_simple
        id_simple = data[i] if header == PRODUCT_ID['header'] else id_simple

    if not sku_simple or not id_simple:
        print('not SKU OR ID')
        return

    # Retrieve or define variant:
    if ProductVariant.objects.filter(
            sku_simple=sku_simple, product__vendor_id=vendor_id).exists():
        product_variant = ProductVariant.objects.get(
            sku_simple=sku_simple, product__vendor_id=vendor_id)
    else:
        sku = sku_simple + '00000' + str(vendor_id)
        product_variant = ProductVariant(sku=sku, sku_simple=sku_simple)

    # Retrieve or define product, aslo check if product id is valid:
    if product_variant.product_id:
        product = product_variant.product
        if id_simple and product_variant.product.id_simple != id_simple:
            raise Exception(
                'el id del producto no corresponde con el producto del variant')
    else:
        vendor = Vendor.objects.get(id=vendor_id)
        product = Product(id_simple=id_simple, vendor=vendor)

    for n, attr_name in enumerate(headers):
        value = data[n]
        try:
            if attr_name == PRODUCT_TYPE_NAME['header']:
                product_type = ProductType.objects.get(
                    name=value)
                product.product_type = product_type
                continue

            if attr_name == PRODUCT_NAME['header']:
                product.__setattr__(PRODUCT_NAME['attribute'], value)
                continue

        except KeyError:
            continue
        else:
            print("no exceptions")
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
