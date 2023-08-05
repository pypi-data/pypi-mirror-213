from datetime import datetime

from prompt_toolkit.token import Token
from PyInquirer import prompt as pi_prompt
from PyInquirer import style_from_dict

PROMPT_STYLE = style_from_dict({
    Token.Separator: "#cc5454",
    Token.QuestionMark: "#673ab7 bold",
    Token.Selected: "#cc5454",  # default
    Token.Pointer: "#673ab7 bold",
    Token.Instruction: "",  # default
    Token.Answer: "#00FFFF bold",
    Token.Question: "",
})


def prompt(questions):
    return pi_prompt(questions, style=PROMPT_STYLE)


def date_validator(*func_args):
    func = func_args[0]
    def wrapper(*args):
        try:
            value = (datetime.strptime(args[0], "%Y-%m-%d").date(), )
        except ValueError:
            return "Please enter a valid date"
        else:
            return func(*value)
    return wrapper


def float_validator(*func_args):
    func = func_args[0]
    def wrapper(*args):
        try:
            value = (float(args[0]), )
        except ValueError:
            return "Please enter a valid number"
        else:
            return func(*value)
    return wrapper


def int_validator(*func_args):
    func = func_args[0]
    def wrapper(*args):
        try:
            value = (int(args[0]), )
        except ValueError:
            return "Please enter a valid number"
        else:
            return func(*value)
    return wrapper
