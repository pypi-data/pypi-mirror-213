from ..controller.base import IProcess

class Default(IProcess):


    def process(self,expression):



        return expression


    def set_successor(self,successor):
        self.successor = successor
