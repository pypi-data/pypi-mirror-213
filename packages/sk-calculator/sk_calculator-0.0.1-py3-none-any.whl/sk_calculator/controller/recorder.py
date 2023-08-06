from ..controller.base import IRecorder

class Recorder(IRecorder):

    def __init__(self):

        self.index = 0

        self.records = {}
        pass




    def record(self,in_exp,out_exp,name=''):

        self.index = self.index+1

        try:
            self.records[self.expression] = self.records[self.expression] +[[self.index,name,in_exp,out_exp]]
        except:
            self.index = 0
            self.records[self.expression] = [[self.index,name,in_exp,out_exp]]

    def get_record(self,expression):


        try:
            for i in self.records[expression]:
                print(i[0],i[1],i[2],i[3])
        except KeyError:
            print("No record found for :",expression)

    def set_expression(self,expression):


        self.expression = expression





