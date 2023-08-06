from ..controller.base import IValidation


class ParenthesesErrorChecker(IValidation):


    def check_error(self,expression):


        open_brackets = expression.count('(')
        close_brackets = expression.count(')')

        if open_brackets>close_brackets:

            self.error_handler.set_error('SyntaxError: Missing Closing Parentheses')

        elif open_brackets<close_brackets:

            self.error_handler.set_error('Syntax Error: Missing Opening Parentheses')

        return self.successor.check_error(expression)


    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler