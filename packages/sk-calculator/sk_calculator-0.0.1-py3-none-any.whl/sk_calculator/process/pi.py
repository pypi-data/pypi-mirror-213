from ..controller.base import IProcess
import regex
import math
class Pi(IProcess):


    def process(self,expression):

        self.expression = expression
        pi = r'\bpi\b'
        self.expression = regex.sub(pi,str(math.pi),self.expression)
        if (regex.match(pi,expression)):
            self.recorder.record('pi',str(math.pi),self.__class__.__name__)
        return self.successor.process(self.expression)


    def set_successor(self,successor):
        self.successor = successor
    def set_recorder(self,recorder):

            self.recorder = recorder