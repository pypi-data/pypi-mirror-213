from ..controller.base import IFunction
import math
class Sqrt(IFunction):

    def evaluate(self,match):
        if match[0] == 'sqrt':

            try:
                value = math.sqrt(float(match[1]))
            except ValueError:
                return self.error_handler.set_error("Math Error: Square Root Of A Negative Number")
            return round(value,9)

        if(self.error_handler.get_error()):
            return self.error_handler.get_error()

        return self.successor.evaluate(match)
    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler
