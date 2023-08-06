from ..controller.base import IOperation
import math
import re
class Power(IOperation):


    def evaluate(self,expression):

        pow_pattern = r'(?<=\d)[\^]'

        match = re.search(pow_pattern,expression)

        if match:
            exp_list = re.split(pow_pattern,expression)
            num_list = []
            for exp in exp_list:
                num_list.append(self.successor.evaluate(exp))

            if(self.handler.get_error()):

                return self.handler.get_error()

            total = float(num_list[0])
            for num in num_list[1:]:
                total = total ** float(num)

            return total


        return self.successor.evaluate(expression)

    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.handler = handler

    def set_recorder(self,recorder):

            self.recorder = recorder