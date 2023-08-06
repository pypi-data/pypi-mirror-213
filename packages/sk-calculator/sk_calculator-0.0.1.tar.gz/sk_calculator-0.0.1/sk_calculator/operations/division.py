from ..controller.base import IOperation
import re
class Division(IOperation):


    def evaluate(self,expression):

        divide_pattern = r'(?<=\d)[/]'

        match = re.search(divide_pattern,expression)

        if match:
            exp_list = re.split(divide_pattern,expression)
            num_list = []
            for exp in exp_list:
                num_list.append(self.successor.evaluate(exp))
            if(self.handler.get_error()):
                return self.handler.get_error()
            try:
                total = float(num_list[0])
                for num in num_list[1:]:
                    total = total / float(num)
            except ZeroDivisionError:
                return self.handler.set_error(f'Math Error: Division by zero at {total}/0')

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