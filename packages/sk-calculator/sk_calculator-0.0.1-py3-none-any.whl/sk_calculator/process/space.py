from ..controller.base import IProcess

class Space(IProcess):


    def process(self,expression):



        expression = expression.replace(" ",'')
        return expression


    def set_successor(self,successor):
        self.successor = successor

    def set_recorder(self,recorder):

            self.recorder = recorder