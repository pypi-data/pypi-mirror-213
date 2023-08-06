from ..controller.base import IValidation
import regex

class DivsionErrorChecker(IValidation):


    def check_error(self,expression):
        division_zero = r'((?:\d+(?:\.\d+)?)/0(?:\.[0]+)?\b)'
        matches = regex.findall(division_zero,expression)
        if matches:
            for match in matches:

                self.error_handler.set_error('Math Error: Division by zero at '+match)

        return self.successor.check_error(expression)



    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler