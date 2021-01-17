class Validator(object):
    def __init__(self, data, n):
        self.data = data
        self.n = n

    def validate(self):
        pass


class ColumnValidator(Validator):

    def validate(self):
        # false si al excel le falta alguna columna:
        # return 'error en ' + self.n
        pass


class SKUValidator(Validator):

    def validate(self):
        pass
