from ..controller.base import IErrorHandler

class ErrorHandle(IErrorHandler):

    def __init__(self):


        self.errors = {}
        self.error = []


    def set_error(self,error):

        try:
            self.errors[self.expression] = self.errors[self.expression]+[error]
        except KeyError:
            self.errors[self.expression] = [error]

        return self.errors[self.expression]

    def get_error(self):

        try:
            return self.errors[self.expression]

        except KeyError:

            return False


    def set_expression(self,expression):

        self.expression = expression
    def get_errors(self):

        for expression,error in self.errors.items():
            print(expression,error)

    def clean_errors(self):
        self.errors ={}




