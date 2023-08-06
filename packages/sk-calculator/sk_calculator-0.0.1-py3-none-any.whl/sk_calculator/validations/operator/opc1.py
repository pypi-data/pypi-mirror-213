from ...controller.base import IValidation
import regex

class Op1(IValidation):


    def check_error(self,expression):


        ## operators like +/
        operators_pattern = r'([\d\.]+)((?:[(+-][*^/])|(?:[+-][*^/)]))'
        matches = regex.findall(operators_pattern,expression)

        if  matches:
            for match in matches:
                self.error_handler.set_error('Syntax Error : Invalid Operators '+match[0]+match[1])

        operators_pattern = r'(\([|^*/%]+)'
        matches = regex.findall(operators_pattern,expression)

        if  matches:
            for match in matches:
                self.error_handler.set_error('Syntax Error : Invalid Operators '+match)


        return self.successor.check_error(expression)



    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler