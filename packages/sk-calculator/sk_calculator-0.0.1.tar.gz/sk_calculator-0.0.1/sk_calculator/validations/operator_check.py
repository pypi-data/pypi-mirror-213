from ..controller.base import IValidation
import regex
from ..validations.operator.opc1 import Op1
from ..validations.operator.opc2 import Op2
from ..validations.operator.opc3 import Op3
from ..validations.operator.opc4 import Op4
from ..validations.operator.opc5 import Op5
from ..validations.default import Default
class OperatorErrorChecker(IValidation):

    def __init__(self):
        self.opc1 = Op1()
        self.opc2 = Op2()
        self.opc3 = Op3()
        self.opc4 = Op4()
        self.opc5 = Op5()
        self.default = Default()


        self.opc1.set_successor(self.opc2)
        self.opc2.set_successor(self.opc3)
        self.opc3.set_successor(self.opc4)
        self.opc4.set_successor(self.opc5)
        self.opc5.set_successor(self.default)



    def check_error(self,expression):

        self.opc1.check_error(expression)

        return self.successor.check_error(expression)



    def set_successor(self,successor):

        self.successor  = successor

    def set_error_handler(self,handler):
        self.error_handler = handler

        self.opc1.set_error_handler(self.error_handler)
        self.opc2.set_error_handler(self.error_handler)
        self.opc3.set_error_handler(self.error_handler)
        self.opc4.set_error_handler(self.error_handler)
        self.opc5.set_error_handler(self.error_handler)
