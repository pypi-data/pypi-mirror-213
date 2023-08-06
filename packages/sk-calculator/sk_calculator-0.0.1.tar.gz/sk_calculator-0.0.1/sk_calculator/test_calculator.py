import unittest
from ..sk_calculator import Calculator
class CalculatorTestCase(unittest.TestCase):


    def setUp(self):
        self.calculator = Calculator()

    def test_evaluate(self):

        # Test evaluate with complex expression

        result = self.calculator.evaluate('200-12/3+3*2*3*7-2+1+2*12-1+7*5')
        self.assertEqual(result, 379)

        # Test evaluate with complex expression
        result = self.calculator.evaluate('2+3+4-1+5')
        self.assertEqual(result, 13)

        # Test evaluate with empty expression
        result = self.calculator.evaluate('')
        self.assertEqual(result, 0)



    def test_evaluate_addition(self):

        result = self.calculator.evaluate('-1+(-2)')
        self.assertEqual(result, -3)

        result = self.calculator.evaluate('1.5+2.3')
        self.assertEqual(result, 3.8)

        result = self.calculator.evaluate('123+456')
        self.assertEqual(result, 579)

        result = self.calculator.evaluate('  1   +   2  ')
        self.assertEqual(result, 3)





    def test_evaluate_subtraction(self):

        result = self.calculator.evaluate('5.2-2.2')
        self.assertEqual(result, 3)

        result = self.calculator.evaluate('5-2-2')
        self.assertEqual(result, 1)

        result = self.calculator.evaluate('-5-2')
        self.assertEqual(result, -7)

    def test_evaluate_multiplication(self):

        result = self.calculator.evaluate('2*3')
        self.assertEqual(result, 6)

    def test_evaluate_division(self):

        result = self.calculator.evaluate('6/2')
        self.assertEqual(result, 3)

        result = self.calculator.evaluate('6.0/01')
        self.assertEqual(result, 6.0)

        result = self.calculator.evaluate('6.0000/000001')
        self.assertEqual(result, 6.0)

        result = self.calculator.evaluate('6.0/01.0')
        self.assertEqual(result, 6.0)

        result = self.calculator.evaluate('0/6')
        self.assertEqual(result, 0)

        result = self.calculator.evaluate('0.0/6')
        self.assertEqual(result, 0.0)



        result = self.calculator.evaluate('2/3')
        self.assertAlmostEqual(result, 0.6666666666666666)

        result = self.calculator.evaluate('2/3.0')
        self.assertAlmostEqual(result, 0.6666666666666666)

        result = self.calculator.evaluate('2.0/3')
        self.assertAlmostEqual(result, 0.6666666666666666)

        result = self.calculator.evaluate('2.0/3.0')
        self.assertAlmostEqual(result, 0.6666666666666666)

        ## division with positive or negative integer

        result = self.calculator.evaluate('6/-2')
        self.assertEqual(result, -3)

        result = self.calculator.evaluate('-6/-2')
        self.assertEqual(result, 3)

        result = self.calculator.evaluate('+6/-2')
        self.assertEqual(result, -3)

        result = self.calculator.evaluate('+6/+2')
        self.assertEqual(result, 3)

        result = self.calculator.evaluate('-6/2')
        self.assertEqual(result, -3)

        result = self.calculator.evaluate('6/-2')
        self.assertEqual(result, -3)

        result = self.calculator.evaluate('-6/-2')
        self.assertEqual(result, 3)

        result = self.calculator.evaluate('+6/-2')
        self.assertEqual(result, -3)

        ## division with positive or negative float
        result = self.calculator.evaluate('+6.0/+2.0')
        self.assertEqual(result, 3)


        self.assertEqual(result, 3)

        result = self.calculator.evaluate('-6.0/2.0')
        self.assertEqual(result, -3.0)

        result = self.calculator.evaluate('+6/2')
        self.assertEqual(result, 3)



        result = self.calculator.evaluate('(-6.0)/(2.0+1)')
        self.assertEqual(result, -2.0)


    def test_evaluate_unary(self):

        result = self.calculator.evaluate('+++5.2---2.2')
        self.assertEqual(result, 3)

        result = self.calculator.evaluate('--5-+2--2')
        self.assertEqual(result, 5)

        result = self.calculator.evaluate('--5/-+5--2')
        self.assertEqual(result, 1)

        result = self.calculator.evaluate('--5-+2/--2')
        self.assertEqual(result, 4)

    def test_evaluate_bracket(self):




        result = self.calculator.evaluate('(-2)')
        self.assertEqual(result, -2)

        result = self.calculator.evaluate('(-2+1)')
        self.assertEqual(result, -1)


        # Test evaluate brackets with complex expression
        result = self.calculator.evaluate('200-(12/3)+(3*2*3*7)-2+1+(2*12)-1+(7*5)')
        self.assertEqual(result, 379)

        # Test evaluate with complex expression
        result = self.calculator.evaluate('(2+3+4)-(1+5)')
        self.assertEqual(result, 3)


        # Test Evaluate brackets with unary operators

        result = self.calculator.evaluate('(+++5.2)-(--2.2)')
        self.assertEqual(result, 3)

        result = self.calculator.evaluate('(--5)-(+2)-(-2)')
        self.assertEqual(result, 5)

        result = self.calculator.evaluate('(--5-+2--2)')
        self.assertEqual(result, 5)

        result = self.calculator.evaluate('-(-5-+2--2)')
        self.assertEqual(result, 5)

        # Test Evaluate Multiple levels of brackets

        result = self.calculator.evaluate('((2+3)+4)-(1+5)')
        self.assertEqual(result, 3)

        #Test Evaluate Complex Multiple Levels of brackets

        result = self.calculator.evaluate('(200-(12/3))+(3*(2*3)*7)-(2+(1))+(2*12)-1+(7*5)')
        self.assertEqual(result, 377)




    def test_evaluate_function(self):



        result = self.calculator.evaluate('sin(0)+cos(0)+tan(0)+cosec(90)+sec(0)+cot(90)')
        self.assertEqual(result, 3)

        result = self.calculator.evaluate('sin(0)+cos(0)+tan(0)+cosec(90)+sec(0)+cot(90)+2')
        self.assertEqual(result, 5)

        ## test sin function

        result = self.calculator.evaluate('sin(0)')
        self.assertEqual(result, 0)

        result = self.calculator.evaluate('sin(30)')
        self.assertEqual(result, 0.5)

        result = self.calculator.evaluate('sin(45)')
        self.assertAlmostEqual(result, 0.7071067812)

        result = self.calculator.evaluate('sin(60)')
        self.assertAlmostEqual(result, 0.8660254)

        result = self.calculator.evaluate('sin(90)')
        self.assertAlmostEqual(result, 1)

        result = self.calculator.evaluate('sin(180)')
        self.assertAlmostEqual(result, 0)

        result = self.calculator.evaluate('sin(270)')
        self.assertAlmostEqual(result, -1)

        result = self.calculator.evaluate('sin(360)')
        self.assertAlmostEqual(result, 0)

        ## test cos function

        result = self.calculator.evaluate('cos(0)')
        self.assertEqual(result, 1)

        result = self.calculator.evaluate('cos(60)')
        self.assertEqual(result, 0.5)

        result = self.calculator.evaluate('cos(45)')
        self.assertAlmostEqual(result, 0.7071067812)

        result = self.calculator.evaluate('cos(30)')
        self.assertAlmostEqual(result, 0.8660254)

        result = self.calculator.evaluate('cos(45)')
        self.assertAlmostEqual(result, 0.7071067812)

        result = self.calculator.evaluate('cos(60)')
        self.assertAlmostEqual(result, 0.5)

        result = self.calculator.evaluate('cos(90)')
        self.assertEqual(result, 0)

        result = self.calculator.evaluate('cos(180)')
        self.assertAlmostEqual(result, -1)

        result = self.calculator.evaluate('cos(270)')
        self.assertAlmostEqual(result, 0)

        result = self.calculator.evaluate('cos(360)')
        self.assertAlmostEqual(result, 1)

        ## test tan function

        result = self.calculator.evaluate('tan(0)')
        self.assertEqual(result, 0)

        result = self.calculator.evaluate('tan(30)')
        self.assertAlmostEqual(result, 0.5773502692)

        result = self.calculator.evaluate('tan(45)')
        self.assertAlmostEqual(result, 1)

        result = self.calculator.evaluate('tan(60)')
        self.assertAlmostEqual(result, 1.732050808)

        result = self.calculator.evaluate('tan(90)')
        self.assertEqual(result, ['Math Error: tan(90.0) is undefined'])

        result = self.calculator.evaluate('tan(180)')
        self.assertEqual(result, 0)

        result = self.calculator.evaluate('tan(270)')
        self.assertEqual(result, ['Math Error: tan(270.0) is undefined'])

        result = self.calculator.evaluate('tan(360)')
        self.assertAlmostEqual(result, 0)

        result = self.calculator.evaluate('tan(810)')
        self.assertEqual(result, ['Math Error: tan(810.0) is undefined'])

        ## test cosec function

        result = self.calculator.evaluate('cosec(0)')
        self.assertEqual(result, ['Math Error: cosec(0.0) is undefined'])

        result = self.calculator.evaluate('cosec(30)')
        self.assertAlmostEqual(result, 2)

        result = self.calculator.evaluate('cosec(45)')
        self.assertAlmostEqual(result, 1.414213562)

        result = self.calculator.evaluate('cosec(60)')
        self.assertAlmostEqual(result, 1.154700538)

        result = self.calculator.evaluate('cosec(90)')
        self.assertEqual(result, 1)

        result = self.calculator.evaluate('cosec(180)')
        self.assertEqual(result, ['Math Error: cosec(180.0) is undefined'])

        result = self.calculator.evaluate('cosec(270)')
        self.assertEqual(result, -1)

        result = self.calculator.evaluate('cosec(360)')
        self.assertEqual(result, ['Math Error: cosec(360.0) is undefined'])

        result = self.calculator.evaluate('cosec(810)')
        self.assertEqual(result, 1)

        ## test cosec function

        result = self.calculator.evaluate('sec(0)')
        self.assertEqual(result, 1)

        result = self.calculator.evaluate('sec(30)')
        self.assertAlmostEqual(result, 1.154700538)

        result = self.calculator.evaluate('sec(45)')
        self.assertAlmostEqual(result, 1.414213562)

        result = self.calculator.evaluate('sec(60)')
        self.assertAlmostEqual(result, 2)



        result = self.calculator.evaluate('sec(180)')
        self.assertEqual(result, -1)

        result = self.calculator.evaluate('sec(270)')
        self.assertEqual(result, ['Math Error: sec(270.0) is undefined'])

        result = self.calculator.evaluate('sec(360)')
        self.assertEqual(result, 1)

        result = self.calculator.evaluate('sec(810)')
        self.assertEqual(result, ['Math Error: sec(810.0) is undefined'])

        ## test cot function

        result = self.calculator.evaluate('cot(0)')
        self.assertEqual(result, ['Math Error: cot(0.0) is undefined'])

        result = self.calculator.evaluate('cot(30)')
        self.assertAlmostEqual(result, 1.732050808)

        result = self.calculator.evaluate('cot(45)')
        self.assertAlmostEqual(result, 1)

        result = self.calculator.evaluate('cot(60)')
        self.assertAlmostEqual(result, 0.577350269)

        result = self.calculator.evaluate('cot(90)')
        self.assertEqual(result, 0)

        result = self.calculator.evaluate('cot(180)')
        self.assertEqual(result, ['Math Error: cot(180.0) is undefined'])

        result = self.calculator.evaluate('cot(270)')
        self.assertEqual(result, 0)

        result = self.calculator.evaluate('cot(360)')
        self.assertEqual(result, ['Math Error: cot(360.0) is undefined'])

        result = self.calculator.evaluate('cot(810)')
        self.assertAlmostEqual(result, 0)


        result = self.calculator.evaluate('sin(-45)')
        self.assertAlmostEqual(result, -0.7071067812)

        result = self.calculator.evaluate('cot(-60)')
        self.assertAlmostEqual(result, -0.577350269)

        result = self.calculator.evaluate('cot(-90)')
        self.assertEqual(result, 0)

        result = self.calculator.evaluate('cot(-135)')
        self.assertAlmostEqual(result, 1)

        result = self.calculator.evaluate('cot(-180)')
        self.assertEqual(result, ['Math Error: cot(-180.0) is undefined'])

        result = self.calculator.evaluate('cot(-225)')
        self.assertAlmostEqual(result, -1)

        result = self.calculator.evaluate('cot(-270)')
        self.assertEqual(result, 0)

        result = self.calculator.evaluate('cot(-315)')
        self.assertAlmostEqual(result, 1)

        result = self.calculator.evaluate('cot(-360)')
        self.assertEqual(result, ['Math Error: cot(-360.0) is undefined'])

        ## trigonometric expressions



        result = self.calculator.evaluate('sin(60) + cos(30) - tan(45) + 10')
        self.assertAlmostEqual(result, 10.732050808)

        result = self.calculator.evaluate('cosec(sin(90)) + sec(cos(0))')
        self.assertAlmostEqual(result, 58.298840823)

        result = self.calculator.evaluate('sin(cos(0+30)) + tan(60) + 5')
        self.assertAlmostEqual(result, 6.747165227)


        ## complex trigonometric expressions

        result = self.calculator.evaluate('sin(90)+cos(90)+sin(1+2)+sin(1+2+(3+4))+cos(sin(90)+cos(-90))')
        self.assertAlmostEqual(result, 2.225831829)

        result = self.calculator.evaluate('sin(cos(tan(45)))')
        self.assertAlmostEqual(result, 0.01744974862)

        result = self.calculator.evaluate('(sin(30) + cos(45)) * 2')
        self.assertAlmostEqual(result, 2.41421356237)


        ## inverse functions

        result = self.calculator.evaluate('asin(1)')
        self.assertAlmostEqual(result, 90)

        result = self.calculator.evaluate('acos(1)')
        self.assertAlmostEqual(result, 0)

        result = self.calculator.evaluate('atan(1)')
        self.assertAlmostEqual(result, 45)

        result = self.calculator.evaluate('acot(1)')
        self.assertAlmostEqual(result, 45)

        result = self.calculator.evaluate('acosec(1)')
        self.assertAlmostEqual(result, 90)

        result = self.calculator.evaluate('asec(1)')
        self.assertAlmostEqual(result, 0)

        result = self.calculator.evaluate('tan(91)')
        self.assertAlmostEqual(result, -57.289961631)

        result = self.calculator.evaluate('tan(271)')
        self.assertAlmostEqual(result, -57.289961631)

        result = self.calculator.evaluate('cot(1)')
        self.assertAlmostEqual(result, 57.289961631)

        result = self.calculator.evaluate('cot(181)')
        self.assertAlmostEqual(result, 57.289961631)

        result = self.calculator.evaluate('sec(91)')
        self.assertAlmostEqual(result, -57.298688499)

        result = self.calculator.evaluate('sec(271)')
        self.assertAlmostEqual(result, 57.298688499)

        result = self.calculator.evaluate('cosec(1)')
        self.assertAlmostEqual(result, 57.298688499)

        result = self.calculator.evaluate('cosec(181)')
        self.assertAlmostEqual(result, -57.298688499)



    def test_evaluate_power(self):

        result = self.calculator.evaluate('2^2')
        self.assertAlmostEqual(result, 4)

        result = self.calculator.evaluate('2^2^2')
        self.assertAlmostEqual(result, 16)

        result = self.calculator.evaluate('2^2^2^2')
        self.assertAlmostEqual(result, 256)

        result = self.calculator.evaluate('(2+2)^(2^2)')
        self.assertAlmostEqual(result, 256)

        result = self.calculator.evaluate('3^2')
        self.assertEqual(result, 9)

        result = self.calculator.evaluate('3^2^2')
        self.assertEqual(result, 81)

        result = self.calculator.evaluate('4^0.5')
        self.assertEqual(result, 2.0)

        result = self.calculator.evaluate('2^(-3+4)')
        self.assertEqual(result, 2)

        result = self.calculator.evaluate('2^(-3)')
        self.assertEqual(result, 0.125)

        result = self.calculator.evaluate('(-2)^3')
        self.assertEqual(result, -8)

        result = self.calculator.evaluate('(-2)^4')
        self.assertEqual(result, 16)

        result = self.calculator.evaluate('(-2)^(-3)')
        self.assertEqual(result, -0.125)

        result = self.calculator.evaluate('(-2)^(-4)')
        self.assertEqual(result, 0.0625)

        result = self.calculator.evaluate('(-2+1+(3^3))-3^2')
        self.assertEqual(result, 17)

    def test_evaluate_square_root(self):



        result = self.calculator.evaluate('sqrt(16)')
        self.assertEqual(result, 4)

        result = self.calculator.evaluate('3 + 2 * (sqrt(16) - 1) / 2 ^ 2')
        self.assertEqual(result, 4.5)

        result = self.calculator.evaluate('(sqrt(25) + sqrt(9)) / 2 * (sqrt(16) - 1) + 5')
        self.assertEqual(result, 17)

        result = self.calculator.evaluate('sqrt(4)')
        self.assertEqual(result, 2)

        result = self.calculator.evaluate('2 * sqrt(9)')
        self.assertEqual(result, 6)

        result = self.calculator.evaluate('sqrt(16) + sqrt(25)')
        self.assertEqual(result, 9)

        result = self.calculator.evaluate('(sqrt(16) + sqrt(9)) / (sqrt(4) - 1)')
        self.assertEqual(result, 7)

        result = self.calculator.evaluate('(sqrt(25) + sqrt(9)) / (sqrt(16) - sqrt(4))')
        self.assertEqual(result, 4)

        result = self.calculator.evaluate('(sqrt(100) - sqrt(81)) * 2')
        self.assertEqual(result, 2)

        result = self.calculator.evaluate('sqrt(16) * sqrt(9)')
        self.assertEqual(result, 12)

        result = self.calculator.evaluate('(sqrt(25) + sqrt(9)) / (2 * sqrt(16) - 1)')
        self.assertEqual(result, 1.1428571428571428)

        result = self.calculator.evaluate('(sqrt(16) + sqrt(9)) / (sqrt(4) + 1)')
        self.assertEqual(result, 2.3333333333333335)

        result = self.calculator.evaluate('sqrt(4) * sqrt(9) + sqrt(16)')
        self.assertEqual(result, 10)

        result = self.calculator.evaluate('sqrt(25) - sqrt(16)')
        self.assertEqual(result, 1)

        result = self.calculator.evaluate('(sqrt(25) + sqrt(9)) / (sqrt(16) - sqrt(4)) * 2')
        self.assertEqual(result, 8)

        result = self.calculator.evaluate('(sqrt(100) - sqrt(81)) * (sqrt(4) + sqrt(9))')
        self.assertEqual(result, 5)

        result = self.calculator.evaluate('sqrt(sqrt(16) + sqrt(9)) / (sqrt(4) + 1) * 2')
        self.assertAlmostEqual(result, 1.76383420738)

    def test_evaluate_log(self):

        result = self.calculator.evaluate('log(10)')
        self.assertEqual(result, 1)

        result = self.calculator.evaluate('log(100)')
        self.assertEqual(result, 2)





    def test_evaluate(self):

        result = self.calculator.evaluate('1+sin(90)+(2*pi)')
        self.assertAlmostEqual(result, 8.283185307179586)

        result = self.calculator.evaluate('((sin(pi/4) + cos(pi/3)) * tan(pi/6)) / log(100) - (sqrt(25) + abs(-7))')
        self.assertAlmostEqual(result, -11.995368740453534)

    def test_evaluate_power(self):
        result = self.calculator.evaluate('2^3')
        self.assertEqual(result, 8)

        result = self.calculator.evaluate('(-2)^3')
        self.assertEqual(result, -8)

        result = self.calculator.evaluate('2^(-3)')
        self.assertAlmostEqual(result, 0.125)

        result = self.calculator.evaluate('(-2)^(-3)')
        self.assertAlmostEqual(result, -0.125)

        result = self.calculator.evaluate('2^0')
        self.assertEqual(result, 1)

        result = self.calculator.evaluate('0^2')
        self.assertEqual(result, 0)

    def test_evaluate_square_root(self):
        result = self.calculator.evaluate('sqrt(16)')
        self.assertEqual(result, 4)

        result = self.calculator.evaluate('sqrt(9)')
        self.assertEqual(result, 3)

        result = self.calculator.evaluate('sqrt(2)')
        self.assertAlmostEqual(result, 1.414213562)

        result = self.calculator.evaluate('sqrt(0)')
        self.assertEqual(result, 0)



    def test_evaluate_exponential(self):
        result = self.calculator.evaluate('exp(1)')
        self.assertAlmostEqual(result, 2.718281828)

        result = self.calculator.evaluate('exp(2)')
        self.assertAlmostEqual(result, 7.389056099)

        result = self.calculator.evaluate('exp(0)')
        self.assertEqual(result, 1)

        result = self.calculator.evaluate('exp(-1)')
        self.assertAlmostEqual(result, 0.3678794412)

        result = self.calculator.evaluate('exp(-2)')
        self.assertAlmostEqual(result, 0.1353352832)

    def test_evaluate_logarithm(self):
        result = self.calculator.evaluate('log(10)')
        self.assertAlmostEqual(result, 1)

        result = self.calculator.evaluate('log(100)')
        self.assertAlmostEqual(result, 2)

        result = self.calculator.evaluate('log(1)')
        self.assertAlmostEqual(result, 0)



        result = self.calculator.evaluate('log(10)')
        self.assertEqual(result, 1)

        result = self.calculator.evaluate('log10(10)')
        self.assertEqual(result, 1)
        result = self.calculator.evaluate('log2(2)')
        self.assertEqual(result, 1)
        result = self.calculator.evaluate('ln(e)')
        self.assertEqual(result, 1)

        result = self.calculator.evaluate('((3.14 * (2 + 5)) / (sqrt(16) + exp(1))) * (sin(0.5) + log10(100)) - (tan(1.5) + (cosec(0.2) * 2)) ^ (acos(0.3) - log2(8))')
        self.assertAlmostEqual(result, -6.425402723271611e+191)


    def test_calculator_complex_operations(self):

        result = self.calculator.evaluate('sqrt((5 - 3)^2 + 4 * 6) / (exp(2) - 1)')
        self.assertAlmostEqual(result, 0.8282135169901252)

        result = self.calculator.evaluate('(sin(0.5) + cos(0.5)) * (tan(0.5) + cot(0.5))')
        self.assertAlmostEqual(result, 115.5930514939486)

        result = self.calculator.evaluate('sqrt(sqrt(sqrt(16) + 1))')
        self.assertAlmostEqual(result, 1.495348781)

        result = self.calculator.evaluate('(-2)^3 + 4 * (2 + 3^2) / 2 - sin(0.5)')
        self.assertAlmostEqual(result, 13.9912734645)

        result = self.calculator.evaluate('sqrt(exp(sqrt(4^2)) + sin(1) - acos(0.5))')
        self.assertEqual(result, ['Math Error: Square Root Of A Negative Number'])

        result = self.calculator.evaluate('tan(0.8) + acos(sin(0.5)) / sqrt(2^3)')
        self.assertAlmostEqual(result, 31.65699200651155)

        result = self.calculator.evaluate('exp(1 + 2^3) - sqrt(cosec(1) + cot(0.5))')
        self.assertAlmostEqual(result, 8089.9733464050005)

    def test_degree_radians(self):

        result = self.calculator.evaluate('sin(pi/2 radians)')
        self.assertAlmostEqual(result, 1)

        result = self.calculator.evaluate('sin(90 degree)')
        self.assertAlmostEqual(result, 1)

        result = self.calculator.evaluate('cos(pi/2 radians)')
        self.assertAlmostEqual(result, 0)

        result = self.calculator.evaluate('cos(90 degree)')
        self.assertAlmostEqual(result, 0)


        result = self.calculator.evaluate('tan(90 degree)')
        self.assertAlmostEqual(result,['Math Error: tan(90.0) is undefined'])

        result = self.calculator.evaluate('tan(pi/2 radians)')
        self.assertAlmostEqual(result, ['Math Error: tan(1.5707963267948966) is undefined'])

        result = self.calculator.evaluate('cosec(90 degree)')
        self.assertAlmostEqual(result, 1)
        result = self.calculator.evaluate('cosec(pi/2 radians)')
        self.assertAlmostEqual(result, 1)

        result = self.calculator.evaluate('sec(90 degree)')
        self.assertAlmostEqual(result,['Math Error: sec(90.0) is undefined'])

        result = self.calculator.evaluate('sec(pi/2 radians)')
        self.assertAlmostEqual(result, ['Math Error: sec(1.5707963267948966) is undefined'])

        result = self.calculator.evaluate('cot(90 degree)')
        self.assertAlmostEqual(result, 0)
        result = self.calculator.evaluate('cot(pi/2 radians)')
        self.assertAlmostEqual(result, 0)

        result = self.calculator.evaluate('sin((pi/2) radians)')
        self.assertAlmostEqual(result, 1)

        result = self.calculator.evaluate('sin(90 degree)+cos(90 degree)+sin(1+2 degree)+sin(1+2+(3+4) degree)+cos(sin(90 degree)+cos(-90 degree) degree)')
        self.assertAlmostEqual(result, 2.225831829)

        result = self.calculator.evaluate('sin(pi/2 radians)+cos(pi/2 radians)+sin(1+2 degree)+sin(1+2+(3+4) degree)+cos(sin(pi/2 radians)+cos(-pi/2 radians) degree)')
        self.assertAlmostEqual(result, 2.225831829)

        result = self.calculator.evaluate('ln(e)+log(10)+log2(2)+sin(pi/2 radians)+cos(pi/2 radians)+sin(1+2 degree)+sin(1+2+(3+4) degree)+cos(sin(pi/2 radians)+cos(-pi/2 radians) degree)')
        self.assertAlmostEqual(result, 5.225831829)



    def test_evaluate_error(self):

        ##Math Error: Division By Zero



        result = self.calculator.evaluate('5/(1-1)')
        self.assertEqual(result, ['Math Error: Division by zero at 5.0/0'])

        result = self.calculator.evaluate('(5 + 2) / ((3 - 1) * (4 - 4))')
        self.assertEqual(result, ['Math Error: Division by zero at 7.0/0'])


        result = self.calculator.evaluate('sec(90)')
        self.assertEqual(result, ['Math Error: sec(90.0) is undefined'])

        result = self.calculator.evaluate('0.0/0')
        self.assertEqual(result, ['Math Error: Division by zero at 0.0/0'])

        result = self.calculator.evaluate('1.000/0')
        self.assertEqual(result, ['Math Error: Division by zero at 1.000/0'])



        result = self.calculator.evaluate('sqrt(-1)')
        self.assertEqual(result, ["Math Error: Square Root Of A Negative Number"])

        result = self.calculator.evaluate('sqrt(/1)')
        self.assertEqual(result, ['Syntax Error : Invalid Operators (/'])

        result = self.calculator.evaluate('sin(/1)')
        self.assertEqual(result, ['Syntax Error : Invalid Operators (/'])

        result = self.calculator.evaluate('sin(0)^0')
        self.assertEqual(result, 1)



        ##Syntaxt Error

        result = self.calculator.evaluate('1+/1')
        self.assertEqual(result, ['Syntax Error : Invalid Operators 1+/'])


        result = self.calculator.evaluate('(-2')
        self.assertEqual(result, ['SyntaxError: Missing Closing Parentheses'])

        result = self.calculator.evaluate('-2)')
        self.assertEqual(result, ['Syntax Error: Missing Opening Parentheses'])

        result = self.calculator.evaluate('1+1*')
        self.assertEqual(result, ['Syntax Error: Incomplete expression at 1*'])

        result = self.calculator.evaluate('(2 + 3))')
        self.assertEqual(result, ['Syntax Error: Missing Opening Parentheses'])

        result = self.calculator.evaluate('sin(cos(2 + 3)')
        self.assertEqual(result, ['SyntaxError: Missing Closing Parentheses'])

        result = self.calculator.evaluate('sin * (2 + 3)')
        self.assertEqual(result, ['Syntax Error: Inappropriate Function Calling sin'])

        result = self.calculator.evaluate('sin(2 + 3) *')
        self.assertEqual(result, ['Syntax Error: Incomplete expression at 3) *'])

        result = self.calculator.evaluate('1 2 3')
        self.assertEqual(result, ['Syntax Error : Invalid Operators 1?2?3'])

        result = self.calculator.evaluate('2@3')
        self.assertEqual(result,['Syntax Error: Unsupported Key @'])

        result = self.calculator.evaluate('x + 5')
        self.assertEqual(result, ['Syntax Error: Invalid Input x'])
        result = self.calculator.evaluate('y + 5')
        self.assertEqual(result, ['Syntax Error: Invalid Input y'])

        result = self.calculator.evaluate(123)
        self.assertEqual(result, ['Invalid Input Type Error'])


        result = self.calculator.evaluate('log(0)')
        self.assertEqual(result, ['Math Error: logarithm of zero'])

        result = self.calculator.evaluate('log(-1)')
        self.assertEqual(result, ['Math Error: logarithm of a negative number'])

        result = self.calculator.evaluate('asin')
        self.assertEqual(result, ['Syntax Error: Inappropriate Function Calling asin'])

        result = self.calculator.evaluate('abc')
        self.assertEqual(result, ['Syntax Error : Unsupported Input abc'])

        result = self.calculator.evaluate('12+28+68+abc')
        self.assertEqual(result, ['Syntax Error : Unsupported Input abc'])

        result = self.calculator.evaluate('12+28+68+(abc)')
        self.assertEqual(result, ['Syntax Error : Unsupported Input abc'])

        result = self.calculator.evaluate('12+21+a')
        self.assertEqual(result, ['Syntax Error: Invalid Input a'])

        result = self.calculator.evaluate('sqrt(-4)')
        self.assertEqual(result, ['Math Error: Square Root Of A Negative Number'])

        result = self.calculator.evaluate('log(0)')
        self.assertEqual(result, ['Math Error: logarithm of zero'])

        result = self.calculator.evaluate('log(-1)')
        self.assertEqual(result, ['Math Error: logarithm of a negative number'])


if __name__ == '__main__':
    unittest.main()
