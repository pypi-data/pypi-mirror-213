from ..controller.base import IFunction
import math
import regex
class Log(IFunction):

    def evaluate(self,match):
        if 'log' in match[0]:
            base_pattern = '[a-zA-Z]+(\d+)'
            base = regex.search(base_pattern,match[0])
            try:
                if match[0]=='log':
                    value = math.log10(float(match[1]))
                elif 'log' in match[0]:
                    value = math.log(float(match[1]),float(base[1]))

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
