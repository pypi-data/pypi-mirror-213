from ...controller.base import IFunction
import math
class Cos(IFunction):


    def evaluate(self,match):
        if match[0] == 'cos':
            cos = math.cos
            deg = math.radians(float(match[1]))
            if match[2]=='degree':
                deg = math.radians(float(match[1]))
            if match[2] == 'radians':
                deg = float(match[1])
            value = cos(deg)
            return  round(value,9)
        if(self.error_handler.get_error()):
            return self.error_handler.get_error()

        return self.successor.evaluate(match)

    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler

