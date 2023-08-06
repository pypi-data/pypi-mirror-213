from ..controller.base import IOperation
import re
class Substraction(IOperation):



    def evaluate(self,expression):

        sub_pattern = r'(?<=\d)-'

        match = re.search(sub_pattern,expression)

        if match:

            exp_list = re.split(sub_pattern,expression)

            num_list = []

            for exp in exp_list:
                num_list.append(self.successor.evaluate(exp))
            total =num_list[0]

            if(self.handler.get_error()):

                return self.handler.get_error()

            for num in num_list[1:]:
                total = total - float(num)

            self.expression = str(total)
            if (self.expression != expression):
                self.recorder.record(expression,self.expression,self.__class__.__name__)
            return total

        return self.successor.evaluate(expression)

    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.handler = handler

    def set_recorder(self,recorder):

            self.recorder = recorder