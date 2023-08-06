from ..controller.base import IValidation
import regex

class NumberChecker(IValidation):


    def check_error(self,expression):


        invalid_num = r'[\d\.]+'
        matches = regex.findall(invalid_num,expression)

        for match in matches:
            if match.count('.')>1:
                self.error_handler.set_error(f"Syntax Error: Invalid number format {match}")



        return self.successor.check_error(expression)



    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler