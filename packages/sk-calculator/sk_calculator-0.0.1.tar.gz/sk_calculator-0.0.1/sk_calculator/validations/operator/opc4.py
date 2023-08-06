from ...controller.base import IValidation
import regex

class Op4(IValidation):


    def check_error(self,expression):


        ## multiple invalid operators at sametime
        operators_pattern = r'([/]{2,}|[*]{2,}|[\^]{2,})'

        matches = regex.findall(operators_pattern,expression)

        if matches:
            for match in matches:
                self.error_handler.set_error('Syntax Error : Invalid Operator '+match)

        return self.successor.check_error(expression)



    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler