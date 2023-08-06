from ..controller.base import IValidation


class Typechecker(IValidation):


    def check_error(self,expression):

        if (type(expression)!=str):

            return self.error_handler.set_error('Invalid Input Type Error')
        if (len(expression)==0):
            return self.error_handler.set_error('Empty Expression')



        return self.successor.check_error(expression)



    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler