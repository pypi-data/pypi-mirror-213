from ..controller.base import IValidation

import regex

class Default(IValidation):


    def check_error(self,expression):


        return expression



    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler