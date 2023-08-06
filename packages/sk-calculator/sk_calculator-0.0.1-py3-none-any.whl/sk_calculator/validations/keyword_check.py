from ..controller.base import IValidation
import regex
from ..controller.function import FunctionHandler
class KeywordChecker(IValidation):


    def check_error(self,expression):
        self.function_handler = FunctionHandler()

        self.valid_functions = {key for key, value in vars(self.function_handler).items() if '__' not in key}


        function_pattern = r'([a-z]+)(\d+(?:\.\d+)?)\s*'
        matches = regex.findall(function_pattern,expression)


        for match in matches:
            if match[0] not in self.valid_functions:
                self.error_handler.set_error('Syntax Error : Invalid keyword '+match[0]+match[1])

        return self.successor.check_error(expression)



    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler