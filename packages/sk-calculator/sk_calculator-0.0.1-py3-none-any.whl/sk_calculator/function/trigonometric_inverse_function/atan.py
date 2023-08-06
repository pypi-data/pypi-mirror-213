from ...controller.base import IFunction
import math
class Atan(IFunction):


    def evaluate(self,match):
        if match[0] == 'atan':
            atan = math.atan
            radian =float(match[1])
            value = atan(radian)
            deg = math.degrees(value)
            return round(deg,9)
        if(self.error_handler.get_error()):
            return self.error_handler.get_error()

        return self.successor.evaluate(match)


    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler

