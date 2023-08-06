from .controller.validation import Validation
from .controller.process import Process
from .controller.function import FunctionHandler
from .controller.error import ErrorHandle
from .controller.bracket import Brackets
from .controller.default import Default
from .controller.recorder import Recorder
from .operations.unary import Unary
from .operations.addition import Addition
from .operations.substraction import Substraction
from .operations.multiplication import Multiplication
from .operations.division import Division
from .operations.power import Power
from .operations.mod import Mod



class Calculator:


    def __init__(self):


        self.error_handle = ErrorHandle()
        self.default  =Default()
        self.division = Division()
        self.power = Power()
        self.mod = Mod()
        self.multiplication = Multiplication()
        self.substraction = Substraction()
        self.addition = Addition()
        self.unary = Unary()
        self.bracket = Brackets()
        self.validation = Validation()
        self.process = Process()
        self.function = FunctionHandler()
        self.recorder = Recorder()

        ## set successor
        self.power.set_successor (self.default)
        self.mod.set_successor (self.power)
        self.division.set_successor (self.mod)
        self.multiplication.set_successor (self.division)
        self.substraction.set_successor ( self.multiplication)
        self.addition.set_successor ( self.substraction)
        self.unary.set_successor(self.addition)
        self.bracket.set_successor(self.unary)
        self.function.set_successor (self.bracket)
        self.process.set_successor (self.function)
        self.validation.set_successor (self.process)

        ## set error handler
        self.division.set_error_handler (self.error_handle)
        self.multiplication.set_error_handler (self.error_handle)
        self.substraction.set_error_handler ( self.error_handle)
        self.addition.set_error_handler (self.error_handle)
        self.unary.set_error_handler(self.error_handle)
        self.bracket.set_error_handler(self.error_handle)
        self.validation.set_error_handler (self.error_handle)
        self.default.set_error_handler(self.error_handle)
        self.power.set_error_handler(self.error_handle)
        self.function.set_error_handler(self.error_handle)
        self.process.set_error_handler(self.error_handle)
        self.mod.set_error_handler(self.error_handle)

        ## set Recorder

        self.division.set_recorder (self.recorder)
        self.multiplication.set_recorder (self.recorder)
        self.substraction.set_recorder ( self.recorder)
        self.addition.set_recorder (self.recorder)
        self.unary.set_recorder(self.recorder)
        self.bracket.set_recorder(self.recorder)
        self.validation.set_recorder (self.recorder)
        self.default.set_recorder(self.recorder)
        self.power.set_recorder(self.recorder)
        self.mod.set_recorder(self.recorder)
        self.function.set_recorder(self.recorder)
        self.process.set_recorder(self.recorder)



    def evaluate(self,expression):

        self.error_handle.set_expression(expression)
        self.recorder.set_expression(expression)
        self.expression =  self.validation.evaluate(expression)
        self.recorder.record(expression,self.expression,self.__class__.__name__)
        return self.expression


__all__ = ['controller', 'function','operations','process','validations']