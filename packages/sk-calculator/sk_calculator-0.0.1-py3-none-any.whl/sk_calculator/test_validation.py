import unittest
from ..sk_calculator.controller.validation import Validation
from ..sk_calculator.calculator.controller.default import Default
from ..sk_calculator.calculator.controller.error import ErrorHandle
class ValidationTestCase(unittest.TestCase):


    def setUp(self):
        self.default = Default()
        self.error_handler = ErrorHandle()
        self.validation = Validation()
        self.validation.set_successor(self.default)
        self.validation.set_error_handler(self.error_handler)
        self.default.set_error_handler(self.error_handler)

    def test_validation(self):

        # Test evaluate with complex expression

        result = self.validation.evaluate('200-12/3+3*2*3*7-2+1+2*12-1+7*5')
        self.assertEqual(result, '200-12/3+3*2*3*7-2+1+2*12-1+7*5')

        # Test evaluate with complex expression
        result = self.validation.evaluate('2+3+4-1+5')
        self.assertEqual(result, '2+3+4-1+5')





        result = self.validation.evaluate('@#$&_|+@#')
        self.assertEqual(result,['Syntax Error: Unsupported Key @#$&_', 'Syntax Error: Unsupported Key @#'])

    def test_type_error(self):

        # Test evaluate with empty expression
        result = self.validation.evaluate('')
        self.assertEqual(result, ['Empty Expression'])

    def test_parentheses_error(self):

        result = self.validation.evaluate('1+(6')
        self.assertEqual(result, ['SyntaxError: Missing Closing Parentheses'])

        result = self.validation.evaluate('1+((6)')
        self.assertEqual(result, ['SyntaxError: Missing Closing Parentheses'])

        result = self.validation.evaluate('1+6)')
        self.assertEqual(result, ['Syntax Error: Missing Opening Parentheses'])

        result = self.validation.evaluate('(200(-12/3+3*2*3*7-(2+1+2*12(-1+7*5')
        self.assertEqual(result, ['SyntaxError: Missing Closing Parentheses'])

        result = self.validation.evaluate('200-(12/(3+3*2*3*7-2+1+2*12-1+7*5')
        self.assertEqual(result, ['SyntaxError: Missing Closing Parentheses'])

        result = self.validation.evaluate('1)')
        self.assertEqual(result, ['Syntax Error: Missing Opening Parentheses'])


    def test_function_error(self):

        result = self.validation.evaluate('sin()')
        self.assertEqual(result, ['Syntax Error: Empty Function Calling sin()'])

        result = self.validation.evaluate('sin()+cos()')
        self.assertEqual(result, ['Syntax Error: Empty Function Calling sin()','Syntax Error: Empty Function Calling cos()'])

        result = self.validation.evaluate('sin(tan())+cos()')
        self.assertEqual(result, ['Syntax Error: Empty Function Calling tan()','Syntax Error: Empty Function Calling cos()'])



    def test_keyword(self):

        result = self.validation.evaluate('sin90')
        self.assertEqual(result, ['Syntax Error: Inappropriate Function Calling sin90'])

        result = self.validation.evaluate('abs90')
        self.assertEqual(result,['Syntax Error: Inappropriate Function Calling abs90'])

        result = self.validation.evaluate('abc90')
        self.assertEqual(result, ['Syntax Error : Invalid keyword abc90'])



        result = self.validation.evaluate('what90')
        self.assertEqual(result, ['Syntax Error : Invalid keyword what90'])

    def test_invalid_operators_error(self):

        result = self.validation.evaluate('1+/1')
        self.assertEqual(result, ['Syntax Error : Invalid Operators 1+/'])

        result = self.validation.evaluate('1+*1')
        self.assertEqual(result, ['Syntax Error : Invalid Operators 1+*'])

        result = self.validation.evaluate('1+^1')
        self.assertEqual(result, ['Syntax Error : Invalid Operators 1+^'])

        result = self.validation.evaluate('1-/1')
        self.assertEqual(result, ['Syntax Error : Invalid Operators 1-/'])

        result = self.validation.evaluate('1-*1')
        self.assertEqual(result, ['Syntax Error : Invalid Operators 1-*'])

        result = self.validation.evaluate('1-^1')
        self.assertEqual(result, ['Syntax Error : Invalid Operators 1-^'])

        result = self.validation.evaluate('1 2   1 1 1 1    1')
        self.assertEqual(result, ['Syntax Error : Invalid Operators 1?2???1?1?1?1????1'])

        result = self.validation.evaluate('(1-)')
        self.assertEqual(result, ['Syntax Error : Invalid Operators 1-)'])

        result = self.validation.evaluate('(23)^1(12+)')
        self.assertEqual(result, ['Syntax Error : Invalid Operators 12+)','Syntax Error : Missing Operator 1?(12'])

        result = self.validation.evaluate('log10(10)+10(10)')
        self.assertEqual(result, ['Syntax Error : Missing Operator 10?(10'])

        result = self.validation.evaluate('pi90')
 ##       self.assertEqual(result, ['Syntax Error: Inappropriate Function Calling sin90'])


    def test_incomplete_expression_error(self):

        result = self.validation.evaluate('1+22+')
        self.assertEqual(result, ['Syntax Error: Incomplete expression at 22+'])

        result = self.validation.evaluate('(23)+')
        self.assertEqual(result, ['Syntax Error: Incomplete expression at (23)+'])

        result = self.validation.evaluate('(23)-')
        self.assertEqual(result, ['Syntax Error: Incomplete expression at (23)-'])

        result = self.validation.evaluate('(23)*')
        self.assertEqual(result, ['Syntax Error: Incomplete expression at (23)*'])

        result = self.validation.evaluate('(23)/')
        self.assertEqual(result, ['Syntax Error: Incomplete expression at (23)/'])

        result = self.validation.evaluate('(23)^')
        self.assertEqual(result, ['Syntax Error: Incomplete expression at (23)^'])

        result = self.validation.evaluate('5+6*')
        self.assertEqual(result, ['Syntax Error: Incomplete expression at 6*'])

        result = self.validation.evaluate('8*-')
        self.assertEqual(result, ['Syntax Error: Incomplete expression at 8*-'])

        result = self.validation.evaluate('(+')
        self.assertEqual(result, ['SyntaxError: Missing Closing Parentheses','Syntax Error: Incomplete expression at (+'])




    def test_division_by_zero(self):

            result = self.validation.evaluate('5/0')
            self.assertEqual(result, ['Math Error: Division by zero at 5/0'])

            result = self.validation.evaluate('6/0')
            self.assertEqual(result,['Math Error: Division by zero at 6/0'])

            result = self.validation.evaluate('6/0.0')
            self.assertEqual(result, ['Math Error: Division by zero at 6/0.0'])

            result = self.validation.evaluate('6/0.000')
            self.assertEqual(result, ['Math Error: Division by zero at 6/0.000'])

    def test_invalid_function(self):

        result = self.validation.evaluate('atand()')
        self.assertEqual(result,['Syntax Error: Invalid Function atand()'])



        result = self.validation.evaluate('ads()')
        self.assertEqual(result,['Syntax Error: Invalid Function ads()'])


    def test_missing_operand(self):
        result = self.validation.evaluate('2+')
        self.assertEqual(result, ['Syntax Error: Incomplete expression at 2+'])

        result = self.validation.evaluate('3*')
        self.assertEqual(result, ['Syntax Error: Incomplete expression at 3*'])

        result = self.validation.evaluate('4/')
        self.assertEqual(result, ['Syntax Error: Incomplete expression at 4/'])

    def test_invalid_number_format(self):
        result = self.validation.evaluate('1.23.45')
        self.assertEqual(result, ['Syntax Error: Invalid number format 1.23.45'])

        result = self.validation.evaluate('1..2')
        self.assertEqual(result, ['Syntax Error: Invalid number format 1..2'])

    def test_invalid_variable(self):
        result = self.validation.evaluate('$var+23+333')
        self.assertEqual(result, ['Syntax Error: Unsupported Key $'])

        result = self.validation.evaluate('_abc')
        self.assertEqual(result, ['Syntax Error : Unsupported Input _abc'])

        result = self.validation.evaluate('var+123')
        self.assertEqual(result,['Syntax Error : Unsupported Input var+123'])

        result = self.validation.evaluate('/2')
        self.assertEqual(result,['Syntax Error : Invalid Operator at beganing /'])




if __name__ == '__main__':
    unittest.main()
