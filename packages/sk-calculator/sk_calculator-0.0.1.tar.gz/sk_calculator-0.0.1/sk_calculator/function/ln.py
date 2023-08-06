from ..controller.base import IFunction
import math
import regex
class Ln(IFunction):

    def evaluate(self,match):
        if match[0]=='ln' :
            try:
                value = math.log(float(match[1]))
            except ValueError:
                if (float(match[1])==0):
                    return self.error_handler.set_error("Math Error: logarithm of zero")

                return self.error_handler.set_error("Math Error: logarithm of a negative number")
            return round(value,9)

        if(self.error_handler.get_error()):
            return self.error_handler.get_error()

        return self.successor.evaluate(match)
    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler
