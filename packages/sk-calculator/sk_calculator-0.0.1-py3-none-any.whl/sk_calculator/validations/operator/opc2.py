from ...controller.base import IValidation
import regex

class Op2(IValidation):


    def check_error(self,expression):



        operators_pattern = r'[\d\.]+(?:[\s)]+[\d\.]+)+'
        matches = regex.findall(operators_pattern,expression)

        if  matches:
            for match in matches:
                self.error_handler.set_error('Syntax Error : Invalid Operators '+match.replace(' ','?'))

        return self.successor.check_error(expression)



    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler