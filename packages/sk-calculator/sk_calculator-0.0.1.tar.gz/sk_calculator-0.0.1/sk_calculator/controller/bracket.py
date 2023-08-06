from ..controller.base import IOperation
import re
class Brackets(IOperation):


    def evaluate(self,expression):

        self.expression = expression

        brackets = r'\([^()]+\)'
        matches = re.findall(brackets,self.expression)



        if matches:
            while matches:
                expression = self.expression
                for match in matches:
                    exp =match.replace('(','').replace(')','')
                    evl = self.successor.evaluate(exp)
                    self.expression = self.expression.replace(match,str(evl))
                    self.recorder.record(match,evl,self.__class__.__name__)
                brackets = r'\([^()]+\)'

                matches = re.findall(brackets,str(self.expression))
        if(self.handler.get_error()):

                return self.handler.get_error()


        return self.successor.evaluate(self.expression)


    def set_successor(self,successor):
        self.successor  = successor

    def set_error_handler(self,handler):
        self.handler = handler
    def set_recorder(self,recorder):

            self.recorder = recorder
