# Py-MathParser

Py-MathParser is a Python binding for MathParser (https://github.com/KJ002/MathParser/). This module allows for a simple and quick evaluation of strings. It allows you to evaluate a string with security, you define the external variables!

## Examples

### Basic Eval
```py
result: float = MathParser.evaluate("1+1") # returns 2
```

### Basic Eval (With MathParser Class)
```py
parser = MathParser.Parser()
rpn: MathParser.mp_RPN = parser.reverse_polish_notation("1+1")

result: float = parser.eval(rpn) # returns 2
```
### External Variable Eval
```py
parser = MathParser.Parser()

x: int = 20

parser.append_variable("x", x)

rpn: MathParser.mp_RPN = parser.reverse_polish_notation("1+x")

result: float = parser.eval(rpn) # returns 21
```
### Updating External Variable Eval
```py
parser = MathParser.Parser()

x: int = 20

parser.append_variable("x", x)

rpn: MathParser.mp_RPN = parser.reverse_polish_notation("1+x")

result1: float = parser.eval(rpn) # returns 21

x: int = 10

parser.append_variable("x", x)

result2: float = parser.eval(rpn) # returns 11
```
### Functions Eval
```py
parser = MathParser.Parser()
rpn: MathParser.mp_RPN = parser.reverse_polish_notation("sin(1.5707963267948966)")

result: float = parser.eval(rpn) # returns 1
```
