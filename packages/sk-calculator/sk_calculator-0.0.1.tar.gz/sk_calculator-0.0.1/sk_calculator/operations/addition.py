from ..controller.base import IOperation
import re
class Addition(IOperation):


    def evaluate(self,expression):

        add_pattern = r'(?<=\d)[+]'

        match = re.search(add_pattern,expression)

        if match:

            exp_list = re.split(add_pattern,expression)
            num_list = []
            for exp in exp_list:
                num_list.append(self.successor.evaluate(exp))
            total =num_list[0]

            if(self.error_handler.get_error()):

                return self.error_handler.get_error()

            for num in num_list[1:]:

                total = total + float(num)
                self.expression = str(total)
            if (self.expression != expression):
                self.recorder.record(expression,self.expression,self.__class__.__name__)
            return total

        return self.successor.evaluate(expression)

    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler
    def set_recorder(self,recorder):

            self.recorder = recorder
