from ..controller.base import IValidation
import regex

class UnsupportedKeyCheck(IValidation):


    def check_error(self,expression):


        incomplete_pattern = r'[@#$&_|~`"]+(?:\b|$)'
        matches = regex.findall(incomplete_pattern,expression)
        if matches:
            for match in matches:
                self.error_handler.set_error('Syntax Error: Unsupported Key '+match)

        return self.successor.check_error(expression)



    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler