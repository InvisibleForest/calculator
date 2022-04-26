import calculator
from decimal import Decimal
assert calculator.calculate('2+2') == 4
assert calculator.calculate('1-1') == 0
assert calculator.calculate('10/2') == 5
assert calculator.calculate('4*3') == 12
assert calculator.calculate('3^3') == 27
assert calculator.calculate('2+2*2') == 6
assert calculator.calculate('-13+5') == -8
assert calculator.calculate('-13-999999999') == -1000000012
assert calculator.calculate('√9') == 3
assert calculator.calculate('√9*10') == 30
assert calculator.calculate('0,3+0,3+0,3') == Decimal('0.9')
assert calculator.calculate('2,2+23') == Decimal('25.2')
assert calculator.calculate('5*2+10') == 20
assert calculator.calculate('(6+10-4)/(1+1*2)+1') == 5
assert calculator.calculate('(8+2*5)/(1+3*2-4)') == 6
assert calculator.calculate('1^5/(5*1)+2') == Decimal('2.2')
assert calculator.calculate('0,+5') == 5
assert calculator.calculate(',+10') == 10
assert calculator.calculate(',+,') == 0
assert calculator.calculate(',5/2') == Decimal('0.25')
assert calculator.calculate('123^0') == 1
assert calculator.calculate('0-5') == -5
assert calculator.calculate('-5+3') == -2
assert calculator.calculate(',') == 0
assert calculator.calculate('(0*1)+(3,123/2)*(9-(3-5))') == Decimal('17.1765')

