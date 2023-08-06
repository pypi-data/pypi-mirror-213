from ..controller.base import IOperation
import re
import math
from ..validations.default import Default
from ..validations.type_check import Typechecker
from ..validations.division_check import DivsionErrorChecker
from ..validations.parentheses_check import ParenthesesErrorChecker
from ..validations.function_check import FunctionErrorChecker
from ..validations.operator_check import OperatorErrorChecker
from ..validations.keyword_check import KeywordChecker
from ..validations.completion_check import CompletionErrorChecker
from ..validations.key_check import UnsupportedKeyCheck
from ..validations.constant_check import ConstantChecker
from ..validations.number_check import NumberChecker

class Validation(IOperation):

    def __init__(self):
        self.default = Default()

        self.type_check = Typechecker()
        self.division_check = DivsionErrorChecker()
        self.parentheses_check = ParenthesesErrorChecker()
        self.function_check = FunctionErrorChecker()
        self.operator_check = OperatorErrorChecker()
        self.keyword_check = KeywordChecker()
        self.completion_check = CompletionErrorChecker()
        self.key_check = UnsupportedKeyCheck()
        self.constant_check = ConstantChecker()
        self.num_check = NumberChecker()



        self.type_check.set_successor(self.parentheses_check)
        self.parentheses_check.set_successor(self.function_check)
        self.function_check.set_successor(self.operator_check)
        self.operator_check.set_successor(self.keyword_check)
        self.keyword_check.set_successor(self.completion_check)
        self.completion_check.set_successor(self.key_check)
        self.key_check.set_successor(self.constant_check)
        self.constant_check.set_successor(self.num_check)
        self.num_check.set_successor(self.division_check)
        self.division_check.set_successor(self.default)






    def evaluate(self,expression):



        self.error_handler.set_expression(expression)

        self.type_check.check_error(expression)

        if(self.error_handler.get_error()):

            return self.error_handler.get_error()




        return self.successor.evaluate(expression)

    def set_successor(self,successor):

        self.successor  = successor


    def set_error_handler(self,handler):

        self.error_handler = handler
        self.type_check.set_error_handler(self.error_handler)
        self.division_check.set_error_handler(self.error_handler)
        self.parentheses_check.set_error_handler(self.error_handler)
        self.function_check.set_error_handler(self.error_handler)
        self.operator_check.set_error_handler(self.error_handler)
        self.keyword_check.set_error_handler(self.error_handler)
        self.completion_check.set_error_handler(self.error_handler)
        self.key_check.set_error_handler(self.error_handler)
        self.constant_check.set_error_handler(self.error_handler)
        self.num_check.set_error_handler(self.error_handler)

    def set_recorder(self,recorder):

            self.recorder = recorder





