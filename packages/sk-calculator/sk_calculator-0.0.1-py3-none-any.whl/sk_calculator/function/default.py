from ..controller.base import IFunction
import re
class Default(IFunction):

    def evaluate(self,exp):

        if  ' ' in exp or exp == '':
            return exp
        try:
            exp = float(exp)
        except TypeError:
            if (len(exp[0])!=1):
                match = exp
                error = 'Invalid Function Error : '+ match[0]+'()'
                return self.error_handler.set_error(error)
            error = 'Undefined Variable Error : ' + exp[0]
            return self.error_handler.set_error(error)

        return exp

    def set_successor(self):
        pass

    def set_error_handler(self,handler):
        self.error_handler = handler