from ...controller.base import IValidation
import regex

class Op3(IValidation):


    def check_error(self,expression):


        ## missing operator between brackets and numbers

        operators_pattern = '(log)?(\d+(?:\.\d+)?)\((\d+(?:\.\d+)?)'

        matches = regex.findall(operators_pattern,expression)

        if matches:
            for match in matches:
                if match[0] == 'log':
                    pass
                else:
                    self.error_handler.set_error('Syntax Error : Missing Operator '+match[1]+'?('+match[2])
        return self.successor.check_error(expression)



    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler