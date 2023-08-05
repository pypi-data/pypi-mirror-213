# Simple Python Math Calculator

This package is a simple math calculator. It has basic operations such as addition, subtraction,
multiplication, and division. Additionally, it also has the ability to find the nth root. This calculator
will store all values computed until the memory is reset.

## Installation

Installing tcCalc3 with pip

`pip install tcCalc3`

## Features

- Addition
- Subtraction
- Multiplication
- Division
- nth Root

## Methods

**.memory()** - *Return the current value stored in the calculator's memory*

**.add(num)**- *Add value to the calculator's current value.*
   
**.subtract(num)** - *Subtract value from the calculator's current value.*

**.multiply(num)** - *Multiply value of the calculator's current value.*

**.divide(num)** - *Divide value of the calculator's current value.*

**.nroot(num, n)** - *Calculate the nth root of a number.*

**.reset()** - *Reset the calculators value in memory back to zero.*


## Usage

```
from tcCalc.calculator import Calculator

# Initialize instance
calculator = Calculator()

# Calling the methods

>>> calculator.add(10)
10

>>> calculator.subtract(3)
7

>>> calculator.multiply(3)
21

>>> calculator.divide(3)
7

>>> calculator.nroot(81,2)
9

>>> calculator.memory()
7

>>> calculator.reset()
0

```