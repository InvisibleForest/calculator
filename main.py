from PyQt5 import QtCore, QtWidgets
from calculatorui import Ui_MainWindow
import calculator as calc
import sys
import re


def show_answer(row_expression) -> None:
    """Receiving showed expression, sending it to calculate and
    displaying calculated answer. If error appears, displaying
    error text"""
    try:
        ui.equal_clicked = True
        answer = str(calc.calculate(row_expression))
        answer = answer.replace('.', ',')
        answer = re.sub(',0*$', '', answer)
        show_text(answer)
    except ZeroDivisionError:
        show_text('Zero Division')
        QtCore.QTimer.singleShot(500, clear_display)
    except ValueError as ve:
        show_text(*ve.args)
        QtCore.QTimer.singleShot(1000, clear_display)
    except (ArithmeticError, IndexError):
        show_text('Error')
        QtCore.QTimer.singleShot(500, clear_display)


def show_digit(digit: str) -> None:
    """Receiving digit and displaying it."""
    clear_display_for_new_expression()
    text = ui.text_window.text()
    if text == '0':
        show_text(digit)
    else:
        show_text(text + digit)


def show_brace(brace: str) -> None:
    """Receiving brace and display it"""
    clear_display_for_new_expression()
    text = ui.text_window.text()
    if brace == '(':
        if not text or text[-1] in '+-*/^(√':
            show_text(text + brace)
        elif text[-1].isdigit():
            show_text(text + '*' + brace)
    elif brace == ')':
        if text.count('(') > text.count(')'):
            show_text(text + brace)


def show_operand(operand):
    """Receiving operand (+-*/^) and displaying it.
    If last symbol in expression is operand,
    changing it with the received operand
    """
    ui.equal_clicked = False
    text = ui.text_window.text()
    if text and text[-1] in '+-*/^':
        show_text(text[:-1] + operand)
    else:
        show_text(text + operand)


def show_comma():
    """Displaying comma. If comma placed without whole number part,
    func adds zero before comma.
    """
    clear_display_for_new_expression()
    text = ui.text_window.text()
    operand_index = 0
    for elem in '+-*/^':
        founded_index = text.rfind(elem)
        if founded_index > operand_index:
            operand_index = founded_index
    if not text:
        show_text(text + '0,')
    elif ',' not in text[operand_index:]:
        if text[operand_index:][-1] in '+-*/^':
            show_text(text + '0,')
        else:
            show_text(text + ',')


def backspace():
    """Deleting last symbol from expression"""
    text = ui.text_window.text()[:-1]
    if text:
        show_text(text)
    else:
        ui.text_window.setText('')


def show_root():
    """Displaying root symbol"""
    clear_display_for_new_expression()
    text = ui.text_window.text()
    show_text(text + '√')


def clear_display():
    """Removing whole expression"""
    ui.text_window.setText('')


def clear_display_for_new_expression():
    """Clearing display after calculation for showing new
    expression. If equal button flag was pressed,
    clearing display and switching the flag"""
    if ui.equal_clicked:
        clear_display()
        ui.equal_clicked = False


def show_text(text: str) -> None:
    """Displaying expression or number in the calculator window.
    Changing shown text size in order to fit the window's size"""
    style_sheet = ui.text_window.styleSheet()
    if len(text) < 15:
        style_sheet = re.sub(r'font: \d+pt', 'font: 16pt', style_sheet)
    elif 15 <= len(text) < 21:
        style_sheet = re.sub(r'font: \d+pt', 'font: 12pt', style_sheet)
    elif 21 <= len(text) < 32:
        style_sheet = re.sub(r'font: \d+pt', 'font: 8pt', style_sheet)
    elif len(text) >= 32:
        style_sheet = re.sub(r'font: \d+pt', 'font: 7pt', style_sheet)
    ui.text_window.setStyleSheet(style_sheet)
    ui.text_window.setText(text)


# preparing and showing ui
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

# flag that functions will use when displaying text
ui.equal_clicked = False

# connecting buttons to functions
ui.btn_0.clicked.connect(lambda: show_digit('0'))
ui.btn_1.clicked.connect(lambda: show_digit('1'))
ui.btn_2.clicked.connect(lambda: show_digit('2'))
ui.btn_3.clicked.connect(lambda: show_digit('3'))
ui.btn_4.clicked.connect(lambda: show_digit('4'))
ui.btn_5.clicked.connect(lambda: show_digit('5'))
ui.btn_6.clicked.connect(lambda: show_digit('6'))
ui.btn_7.clicked.connect(lambda: show_digit('7'))
ui.btn_8.clicked.connect(lambda: show_digit('8'))
ui.btn_9.clicked.connect(lambda: show_digit('9'))
ui.btn_open_brace.clicked.connect(lambda: show_brace('('))
ui.btn_close_brace.clicked.connect(lambda: show_brace(')'))
ui.btn_minus.clicked.connect(lambda: show_operand('-'))
ui.btn_plus.clicked.connect(lambda: show_operand('+'))
ui.btn_divide.clicked.connect(lambda: show_operand('/'))
ui.btn_mul.clicked.connect(lambda: show_operand('*'))
ui.btn_pow.clicked.connect(lambda: show_operand('^'))
ui.btn_root.clicked.connect(show_root)
ui.btn_comma.clicked.connect(lambda: show_comma())
ui.btn_backspace.clicked.connect(backspace)
ui.btn_clear.clicked.connect(clear_display)
ui.btn_equal.clicked.connect(lambda: show_answer(ui.text_window.text()))

sys.exit(app.exec_())
