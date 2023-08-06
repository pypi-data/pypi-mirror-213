from ..controller.base import IValidation
import regex
from ..controller.function import FunctionHandler
class FunctionErrorChecker(IValidation):


    def check_error(self, expression):
        self.function_handler = FunctionHandler()
        self.valid_functions = {key for key, value in vars(self.function_handler).items() if '__' not in key}
        function_pattern = r'([a-zA-Z]+\d*)(\((?>[^()a-zA-Z]|(?2))*([a-zA-Z]+)?\))'

        matches = regex.findall(function_pattern, expression)

        if matches:
            for match in matches:
                empty_call = '\(\s*\)'
                if match[0] not in self.valid_functions and 'log' not in match[0]:
                    self.error_handler.set_error(f'Syntax Error: Invalid Function {match[0]}()')

                elif regex.match(empty_call,match[1]):
                    self.error_handler.set_error(f'Syntax Error: Empty Function Calling {match[0]}()')

        inapro_function = r'([a-zA-Z]+)(\d+(?:\.\d+)?)?(\s*[(])?'
        matches = regex.findall(inapro_function,expression)

        for match in matches:
            if match[0] in self.valid_functions and 'log' not in match[0] and '(' != match[2]:

                self.error_handler.set_error(f'Syntax Error: Inappropriate Function Calling {match[0]+match[1]}')




        return self.successor.check_error(expression)


    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler