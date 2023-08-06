from controller.base import IOperation
import re
class Brackets(IOperation):


    def evaluate(self,expression):

        brackets = r'\([^()]+\)'
        matches = re.findall(brackets,expression)



        if matches:
            while matches:
                for match in matches:
                    exp =match.replace('(','').replace(')','')
                    evl = self.successor.evaluate(exp)
                    expression = expression.replace(match,str(evl))
                brackets = r'\([^()]+\)'
                matches = re.findall(brackets,str(expression))


        return self.successor.evaluate(expression)


    def set_successor(self,successor):
        self.successor  = successor

    def set_error_handler(self,handler):
        self.handler = handler
    def set_recorder(self,recorder):

            self.recorder = recorder