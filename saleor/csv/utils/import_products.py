from openpyxl import load_workbook


def import_products_from_xlsx(filename):
    wb = load_workbook(filename=filename)
    return wb
