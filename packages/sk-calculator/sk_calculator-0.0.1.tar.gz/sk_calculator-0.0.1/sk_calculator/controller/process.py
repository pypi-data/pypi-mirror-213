from ..controller.base import IOperation

from ..process.pi import Pi
from ..process.e import E
from ..process.space import Space
from ..process.default import Default

class Process(IOperation):

    def __init__(self):

        self.pi = Pi()
        self.e = E()
        self.__space = Space()
        self.__default = Default()


        self.pi.set_successor(self.e)
        self.e.set_successor(self.__space)
        self.__space.set_successor(self.__default)


    def evaluate(self,expression):

        self.expression = self.pi.process(expression)
        return self.successor.evaluate(self.expression)






    def set_successor(self,successor):
        self.successor  = successor

    def set_error_handler(self,handler):
        self.handler = handler

    def set_recorder(self,recorder):

            self.recorder = recorder
            self.pi.set_recorder(self.recorder)
            self.e.set_recorder(self.recorder)
            self.__space.set_recorder(self.recorder)

