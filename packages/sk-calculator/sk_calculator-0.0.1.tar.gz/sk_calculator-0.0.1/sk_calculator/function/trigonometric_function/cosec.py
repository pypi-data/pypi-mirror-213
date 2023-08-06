from ...controller.base import IFunction
import math
class Cosec(IFunction):


    def evaluate(self,match):
        if match[0] == 'cosec':
            n =float(match[1]) /  90
            if match[2] == 'radians':
                n = float(match[1])/(math.pi/2)
            if n%2 == 0:
                return self.error_handler.set_error(f'Math Error: {match[0]}({match[1]}) is undefined')
            sin = math.sin
            deg = math.radians(float(match[1]))
            if match[2]=='degree':
                deg = math.radians(float(match[1]))
            if match[2] == 'radians':
                deg = float(match[1])
            value = 1/sin(deg)
            return round(value,9)
        if(self.error_handler.get_error()):
            return self.error_handler.get_error()

        return self.successor.evaluate(match)



    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler

