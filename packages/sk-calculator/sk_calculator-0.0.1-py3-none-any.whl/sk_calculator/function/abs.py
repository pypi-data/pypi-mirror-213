from ..controller.base import IFunction
class Abs(IFunction):

    def evaluate(self,match):
        if match[0] == 'abs':

            try:
                value = abs(float(match[1]))
            except ValueError:
                return self.error_handler.set_error("Math Error : Invalid type")
            return round(value,9)

        if(self.error_handler.get_error()):
            return self.error_handler.get_error()

        return self.successor.evaluate(match)
    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler
