from ..controller.base import IOperation
import re
class Default(IOperation):

    def evaluate(self,exp):
        try:
            exp = float(exp)

        except ValueError:
            pattern = r'[a-zA-Z]+'
            match = re.search(pattern,exp)
            error = exp
            if match:
                error = 'Syntax Error : Unsupported Input '
                return self.error_handler.set_error(error+exp)
            return exp
        return exp

    def set_successor(self):
        pass

    def set_error_handler(self,handler):
        self.error_handler = handler
    def set_recorder(self,recorder):

            self.recorder = recorder
