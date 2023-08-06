from ..controller.base import IOperation
import re
import regex
import math

from ..function.trigonometric_function.sin import Sin
from ..function.trigonometric_function.cos import Cos
from ..function.trigonometric_function.tan import Tan
from ..function.trigonometric_function.cosec import Cosec
from ..function.trigonometric_function.sec import Sec
from ..function.trigonometric_function.cot import Cot
from ..function.trigonometric_inverse_function.asin import Asin
from ..function.trigonometric_inverse_function.acos import Acos
from ..function.trigonometric_inverse_function.atan import Atan
from ..function.trigonometric_inverse_function.acosec import Acosec
from ..function.trigonometric_inverse_function.asec import Asec
from ..function.trigonometric_inverse_function.acot import Acot
from ..function.sqrt import Sqrt
from ..function.abs import Abs
from ..function.exp import Exp
from ..function.log import Log
from ..function.ln import Ln
from ..function.default import Default
from ..controller.error import ErrorHandle

class FunctionHandler(IOperation):

    def __init__(self):

        self.sin = Sin()
        self.cos = Cos()
        self.tan = Tan()
        self.tan = Tan()
        self.cosec = Cosec()
        self.sec = Sec()
        self.cot = Cot()
        self.sqrt = Sqrt()
        self.abs = Abs()
        self.log = Log()
        self.ln = Ln()
        self.exp = Exp()

        ## inverse trigonometric functinos
        self.asin = Asin()
        self.acos = Acos()
        self.atan = Atan()
        self.acosec = Acosec()
        self.asec = Asec()
        self.acot = Acot()
        self.__default = Default()


        self.exp.set_successor(self.abs)
        self.abs.set_successor(self.log)
        self.log.set_successor(self.ln)
        self.ln.set_successor(self.sqrt)
        self.sqrt.set_successor(self.sin)
        self.sin.set_successor(self.cos)
        self.cos.set_successor(self.tan)
        self.tan.set_successor(self.cosec)
        self.cosec.set_successor(self.sec)
        self.sec.set_successor(self.cot)
        self.cot.set_successor(self.asin)

        self.asin.set_successor(self.acos)
        self.acos.set_successor(self.atan)
        self.atan.set_successor(self.acosec)
        self.acosec.set_successor(self.asec)
        self.asec.set_successor(self.acot)
        self.acot.set_successor(self.__default)

    def evaluate(self,expression):

        self.__expression = expression
       ## find all trigonometric function

        funtion_pattern = r'([a-zA-Z]+\d*)(\((?>[^()a-zA-Z]|(?2))*([a-zA-Z]+)?\))'
        matches = regex.findall(funtion_pattern,self.__expression)

        while matches:
            for match in matches:
                function = match[0].lower()
                argument=self.__successor.evaluate(match[1].replace(match[2],''))
                unit = match[2]
                value = self.exp.evaluate([function,argument,unit])
                in_exp = match[0]+match[1]+match[2]
                self.__recorder.record(in_exp,str(value),self.__class__.__name__)
                replacer = regex.escape(match[0]+match[1])
                self.__expression = regex.sub(replacer,str(value),self.__expression)
                if(self.__error_handler.get_error()):
                    return self.__error_handler.get_error()
                matches = regex.findall(funtion_pattern,self.__expression)

        return self.__successor.evaluate(self.__expression)


    def set_successor(self,successor):
        self.__successor  = successor

    def set_error_handler(self,handler):
        self.__error_handler = handler

        self.sqrt.set_error_handler(self.__error_handler)
        self.exp.set_error_handler(self.__error_handler)
        self.abs.set_error_handler(self.__error_handler)
        self.log.set_error_handler(self.__error_handler)
        self.ln.set_error_handler(self.__error_handler)
        self.sin.set_error_handler(self.__error_handler)
        self.cos.set_error_handler(self.__error_handler)
        self.tan.set_error_handler(self.__error_handler)
        self.cosec.set_error_handler(self.__error_handler)
        self.sec.set_error_handler(self.__error_handler)
        self.cot.set_error_handler(self.__error_handler)

        self.__default.set_error_handler(self.__error_handler)
        self.asin.set_error_handler(self.__error_handler)
        self.acos.set_error_handler(self.__error_handler)
        self.atan.set_error_handler(self.__error_handler)
        self.acosec.set_error_handler(self.__error_handler)
        self.asec.set_error_handler(self.__error_handler)
        self.acot.set_error_handler(self.__error_handler)

    def set_recorder(self,recorder):

            self.__recorder = recorder


