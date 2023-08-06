from ...controller.base import IFunction
import math
class Acot(IFunction):


    def evaluate(self,match):
        if match[0] == 'acot':
            try:
                atan = math.atan
                deg = float(match[1])
                value = atan(1/deg)
                degr = math.degrees(value)
                return round(degr,9)
            except ValueError:
                self.error_handler.set_error(f'Math Error : Math Domain Error at {match[0]}({match[1]})')
        if(self.error_handler.get_error()):
            return self.error_handler.get_error()

        return self.successor.evaluate(match)



    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler

