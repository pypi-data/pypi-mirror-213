# Python Calculator Package

##### This package provides a Calculator class with some calculation methods, and output the calculation in the terminal:
 - add(input): add input to current value
 - substract(input): substract current value with the input
 - multiply(input): multiply current value with the input
 - divide(input): divide current value with the input
 - root(input): get the nth(input) root of the current value
 - reset(): reset the calculator to zero

##### 

#### Install:
`pip install -i https://test.pypi.org/simple/ calculator_mcc==0.1.1`**

#### Import:
`from calculator_mcc import Calculator`

#### Example:

calc = Calculator()\
calc.add(10)\
calc.multiply(2)\
calc.reset()\
print(calc)

#### Output In Terminal:
🤖 10\
🤖 20\
🤖 0\
🤖 current_value: 0


#### To Run Unit Test:
`cd calculator_mcc`\
`pytest` 
