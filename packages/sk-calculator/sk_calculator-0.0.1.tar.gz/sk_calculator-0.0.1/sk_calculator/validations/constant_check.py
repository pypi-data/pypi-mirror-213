from ..controller.base import IValidation
import regex
from ..controller.process import Process
class ConstantChecker(IValidation):


    def check_error(self, expression):
        self.process = Process()
        self.valid_constants = {key for key, value in vars(self.process).items() if '__' not in key}
        constant_pattern = r'\b[a-zA-Z]\b'

        matches = regex.findall(constant_pattern, expression)

        if matches:
            for match in matches:
                if match not in self.valid_constants:
                    self.error_handler.set_error(f'Syntax Error: Invalid Input {match}')



        return self.successor.check_error(expression)


    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler