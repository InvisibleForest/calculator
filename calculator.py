from decimal import Decimal
import re


def calculate(row_expression: str) -> Decimal:
    row_expression = to_correct_row_expression(row_expression)
    expression = convert_to_rpn(row_expression)
    numbers_stack = []
    actions = {'+': Decimal.__add__,
               '-': Decimal.__sub__,
               '*': Decimal.__mul__,
               '/': Decimal.__truediv__,
               '^': Decimal.__pow__,
               '√': Decimal.sqrt}

    for token in expression:
        if type(token) == Decimal:
            numbers_stack.append(token)
        elif token == '√':
            number = actions[token](numbers_stack.pop())
            numbers_stack.append(number)
        else:
            right_number = numbers_stack.pop()
            left_number = numbers_stack.pop()
            numbers_stack.append(actions[token](left_number, right_number))

    if len(numbers_stack) > 1:
        raise ArithmeticError

    return numbers_stack[0]


def convert_to_rpn(row_expression: str) -> list:
    """convert user's expression to reverse polish notation"""
    rpn_expression = []
    prec = {'+': 0, '-': 0, '/': 1, '*': 1, '^': 2, '√': 2}
    # splitting expressions to tokens
    row_expression = row_expression.replace(',', '.')
    tokens = re.split(r'([()+\-*^/√]) *', row_expression)

    tokens = [token for token in tokens if token != '']

    def convert_process() -> None:
        """process of converting"""

        actions_stack = []
        for token in tokens:
            token = to_correct_decimal_number(token)

            # checking for numbers
            if re.fullmatch(r'\d+\.?\d*', token):
                rpn_expression.append(Decimal(token))

            # checking for braces
            elif token == '(':
                actions_stack.append(token)
            elif token == ')':
                while actions_stack[-1] != '(':
                    rpn_expression.append(actions_stack.pop())
                actions_stack.pop()

            # checking for priority of operands with operands in stack
            elif actions_stack:
                while actions_stack:
                    last_action = actions_stack[-1]
                    if last_action != '(' and prec[token] <= prec[last_action]:
                        rpn_expression.append(actions_stack.pop())
                    else:
                        break
                actions_stack.append(token)

            # putting operand in empty stack
            else:
                actions_stack.append(token)

        # moving operands from stack to rpn_expression after parsing
        while actions_stack:
            rpn_expression.append(actions_stack.pop())

    convert_process()
    return rpn_expression


def to_correct_row_expression(row_expression: str) -> str:
    """making correct expression from user's expression."""
    row_expression = re.sub(r'(\(-)', r'(0-', row_expression)
    if row_expression.startswith(('+', '-', '*', '/', '^')):
        row_expression = '0' + row_expression
    if row_expression.count('(') > row_expression.count(')'):
        row_expression += ')'
    if row_expression.endswith(('+', '-', '*', '/', '^', '√')):
        row_expression = row_expression[:-1]
    return row_expression


def to_correct_decimal_number(num: str) -> str:
    """making correct number from number that missed
    digits before or after decimal point. If function got operation just
    returns it back"""
    if num.startswith('.'):
        num = '0' + num
    if num.endswith('.'):
        num = num[:-1]
    return num

if __name__ == '__main__':
    expression = input('Please input expression (without spaces): ')
    print(calculate(expression))
