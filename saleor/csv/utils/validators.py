VARIANT_SKU = {"header": "SKU", "attribute": "sku_simple"}


class Validator(object):
    def __init__(self, data, n):
        self.data = data
        self.n = n + 1

    def validate(self):
        pass


class ColumnValidator(Validator):

    def validate(self):
        if not self.data[VARIANT_SKU['header']]:
            return 'falta SKU en linea' + str(self.n)
        # false si al excel le falta alguna columna:
        # return 'error en ' + self.n


class SKUValidator(Validator):

    def validate(self):
        pass

# # variant validations:
# if sku_simple == ' ':
#     raise Exception('invalid SKU')

# if not sku_simple or not id_simple:
#     print('not SKU OR ID')
#     return

# # product validation:
# if id_simple and product_variant.product.id_simple != id_simple:
#     raise Exception('el id del producto no corresponde con el producto del variant')
