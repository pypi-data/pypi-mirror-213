from ..controller.base import IProcess
import regex
import math
class E(IProcess):


    def process(self,expression):

        self.expression = expression
        e = r'\be\b'
        self.expression = regex.sub(e,str(math.e),self.expression)
        if (expression != self.expression):
            self.recorder.record('e',str(math.e),self.__class__.__name__)
        return self.successor.process(self.expression)


    def set_successor(self,successor):
        self.successor = successor
    def set_recorder(self,recorder):

            self.recorder = recorder