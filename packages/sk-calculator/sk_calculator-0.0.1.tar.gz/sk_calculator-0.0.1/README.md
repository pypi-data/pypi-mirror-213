# Calculator

This is a advanced calculator program that can evaluate arithmetic expressions and perform trigonometric calculations. It provides the following functionality:

- Arithmetic operations: addition, subtraction, multiplication, and division
- Support for complex expressions with multiple operators
- Unary operators: positive and negative signs
- Evaluation of expressions inside brackets
- Trigonometric functions: sin, cos, tan, cosec, sec, and cot
- Inverse trigonometric functions: asin, acos, atan

## Getting Started

Install by command
```
pip install sk_calculator
```


## Usage

To evaluate an arithmetic expression, create an instance of the `Calculator` class and call the `evaluate` method, passing the expression as a string parameter. The method will return the result of the evaluation.

Here's an example:

```python
from sk_calculator import Calculator

# Create an instance of the Calculator class
calculator = Calculator()

# Evaluate an arithmetic expression
result = calculator.evaluate('2 + 3 * 4')
print(result)  # Output: 14
```

You can use the `evaluate` method to perform various calculations, including complex expressions and trigonometric functions.

## Supported Operations

### Arithmetic Operations

The calculator supports the following arithmetic operations:

- Addition: `+`
- Subtraction: `-`
- Multiplication: `*`
- Division: `/`
- Power: `^`
- Module: `%`

### Unary Operators

The calculator supports unary operators to represent positive and negative numbers:

- Positive: `+`
- Negative: `-`

### Evaluation of Expressions

The calculator can evaluate complex expressions with multiple operators and parentheses. It follows the standard order of operations (PEMDAS/BODMAS).

Here's an example:

```python
result = calculator.evaluate('(2 + 3) * 4')
print(result)  # Output: 20
```

### Trigonometric Functions

The calculator provides trigonometric functions to calculate sine, cosine, tangent, cosecant, secant, and cotangent. The functions are case-insensitive.

- Sine: `sin`
- Cosine: `cos`
- Tangent: `tan`
- Cosecant: `cosec`
- Secant: `sec`
- Cotangent: `cot`

Here's an example:

```python
result = calculator.evaluate('sin(45) + cos(30)')
print(result)  # Output: 1.573132185
```

### Inverse Trigonometric Functions

The calculator also supports inverse trigonometric functions to calculate arcsine, arccosine, and arctangent. The functions are case-insensitive.

- Arcsine: `asin`
- Arccosine: `acos`
- Arctangent: `atan`
- ArcCosecant: `acosec`
- ArcSecant: `asec`
- ArcCotangent: `acot`

Here's an example:

```python
result = calculator.evaluate('atan(1)')
print(result)  # Output: 45.0
```

### Additional Functions

The calculator also supports the following additional functions:

- Square Root: `sqrt(x)`, where `x` is the number for which you want to calculate the square root. Example: `sqrt(16)` returns `4`.

- Absolute Value: `abs(x)`, where `x` is the number for which you want to calculate the absolute value. Example: `abs(-5)` returns `5`.

- Exponential: `exp(x)`, where `x` is the number for which you want to calculate the exponential value. Example: `exp(2)` returns `7.3890560989306495`.

- Logarithm: `logx(y)`, where `x` is the base and `y` is the number for which you want to calculate the logarithm. Example: `log10(100)` returns `2`.
Here's an example that includes the usage of these additional functions:

```python
result = calculator.evaluate('sqrt(16) + abs(-5) * exp(2)')
print(result)  # Output: 40.945280495
```

## Validations

The supported validations in your `calculator.py` program are designed to check for various types of errors and ensure that the input expression is valid. Here is a description of each supported validation:

1. **Complex Expression**: This validation tests the evaluation of a complex expression involving multiple arithmetic operations. It verifies that the evaluated result matches the expected expression.

2. **Type Error**: This validation checks for an empty expression. If the expression is empty, it returns an error message indicating that the expression is empty.

3. **Parentheses Error**: This validation identifies errors related to parentheses in the expression. It checks for missing or mismatched opening and closing parentheses and returns appropriate error messages.

4. **Function Error**: This validation detects errors related to function calls. It checks for empty function calls and returns an error message indicating that the function call is empty.

5. **Keyword**: This validation verifies the correctness of function names and keywords used in the expression. It checks for inappropriate function calls and invalid keywords, returning corresponding error messages.

6. **Invalid Operators Error**: This validation identifies errors related to invalid operators in the expression. It checks for unsupported or invalid operator combinations and returns error messages indicating the presence of invalid operators.

7. **Incomplete Expression Error**: This validation checks for incomplete expressions, where an operation is missing an operand. It returns error messages indicating the specific location of the incomplete expression.

8. **Division by Zero**: This validation detects division by zero errors in the expression. It checks for divisions where the divisor is zero and returns error messages indicating the division by zero.

9. **Invalid Function**: This validation identifies errors related to invalid function calls. It checks for unsupported or invalid function names and returns error messages indicating the presence of an invalid function call.

10. **Missing Operand**: This validation checks for missing operands in the expression. It detects expressions where an operation is missing one of its operands and returns error messages indicating the location of the missing operand.

11. **Invalid Number Format**: This validation identifies errors related to invalid number formats in the expression. It checks for numbers with incorrect decimal formats and returns error messages indicating the presence of invalid number formats.

12. **Invalid Variable**: This validation detects errors related to unsupported or invalid variable names in the expression. It checks for variables with unsupported characters and returns error messages indicating the presence of an unsupported variable.

These supported validations help ensure that the expression provided to the calculator is well-formed and prevent errors during the evaluation process.



## Unit Tests

The `test_calculator.py` file contains unit tests for the `Calculator` class. You can run these tests to ensure that the calculator functions correctly.

To run the unit tests, execute the following command in the terminal:

```
python -m unittest test_calculator.py
```

The test cases cover various scenarios, including arithmetic operations, evaluation of expressions, unary operators, and trigonometric functions.
