from django.db import models
from django.db.models.fields import BooleanField, IntegerField, CharField
from django.http import HttpResponse, HttpResponseBadRequest
from django.db.models.fields.related import ManyToManyField, ForeignKey

from openpyxl import load_workbook
from saleor.product.models import Product


readed_attributes = {
    "name": "name",
    "category": "category",
    "product type": "product_type",
}


def getForeignObject(ForeignModel, value):
    try:
        if hasattr(ForeignModel, 'slug'):
            return ForeignModel.objects.get(slug=value)
        if hasattr(ForeignModel, 'code'):
            return ForeignModel.objects.get(code=value)
        if hasattr(ForeignModel, 'name'):
            return ForeignModel.objects.get(name=value)
    except ForeignModel.DoesNotExist:
        return None


def row_to_object(Model, headers, data):

    slug = None
    for i, header in enumerate(headers):
        slug = data[i] if header == 'slug' else slug

    if slug is None:
        object = Model()
    elif Model.objects.filter(slug=slug).exists():
        object = Model.objects.get(slug=slug)
    else:
        object = Model(slug=slug)

    for n, attr_name in enumerate(headers):
        # change read attr_name from ImportedProductAttributes to product real attribute:
        try:
            attr_name = readed_attributes[attr_name]
        except KeyError:
            continue
        else:
            print("unexpected error")

        column_type = object._meta.get_field(attr_name)
        value = data[n]

        if isinstance(column_type, ForeignKey) and value:
            model = getForeignObject(column_type.related_model, value)
            if model:
                object.__setattr__(attr_name + '_id', model.id)
        elif isinstance(column_type, ManyToManyField) and value:
            object.save()
            for v in value.split(','):
                model = getForeignObject(column_type.related_model, v)
                if model:
                    object.__getattribute__(attr_name).add(model)
        elif isinstance(column_type, IntegerField) and value:
            object.__setattr__(attr_name, int(value))
        elif isinstance(column_type, BooleanField):
            object.__setattr__(attr_name, True if value.lower() == 'yes' else False)
        elif isinstance(column_type, CharField):
            object.__setattr__(attr_name, value if value else '')
        elif value:
            object.__setattr__(attr_name, value)

    object.save()
    for n, attr_name in enumerate(headers):

        # change read attr_name from ImportedProductAttributes to product real attribute:
        try:
            attr_name = readed_attributes[attr_name]
        except KeyError:
            continue
        else:
            print("unexpected error")

        column_type = object._meta.get_field(attr_name)
        value = data[n]

        if isinstance(column_type, ManyToManyField) and value:
            for item in value.split(','):
                model = getForeignObject(column_type.related_model, item)
                if model:
                    getattr(object, attr_name).add(model)

    object.save()


def verify_products_from_xlsx(filename):
    try:
        wb = load_workbook(filename=filename)
    except:
        return (False, "fail reason")

    return (True, "no errors")


def import_products_from_xlsx(filename):
    verify_products_from_xlsx(filename=filename)
    wb = load_workbook(filename=filename)
    ws = wb.active

    headers = []
    for n, row in enumerate(ws.iter_rows()):
        data = []
        for cell in row:
            headers.append(cell.value) if n == 0 else data.append(cell.value)

        if len(data):
            row_to_object(Product, headers, data)
        try:
            pass
        except Exception as e:
            raise e
            return HttpResponseBadRequest(str(e))
    return HttpResponse('File imported successfully')
