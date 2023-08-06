from ..controller.base import IOperation
import re
class Unary(IOperation):



    def evaluate(self,expression):

        self.expression = expression

        ## check how many operators present at a time
        pattern = r'[+-]*'
        matches = re.findall(pattern,self.expression)
        matches = list(set(matches))
        for match in matches:
            replacement = match
            sign =replacement.count('+')+ replacement.count('-')
            while sign>1:
                replacement = replacement.replace('++','+').replace('-+','-').replace('+-','-').replace('--','+')
                sign =replacement.count('+')+ replacement.count('-')
            self.expression = self.expression.replace(match,replacement)
        return self.successor.evaluate(self.expression)

    def set_successor(self,successor):

        self.successor  = successor
    def set_error_handler(self,handler):
        self.handler = handler
    def set_recorder(self,recorder):

            self.recorder = recorder
