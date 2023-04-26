# https://leetcode.com/problems/basic-calculator/solutions/1662949/python-actually-working-shunting-yard-that-passes-all-edge-cases/

from machine import Stack
import re
EPSILON = 'ε'
PRECEDENCE = {'|': 1, '%': 1, '?': 2, '@': 2, '#': 2}


# Shunting Yard algorithm
def shunting_yard(expression):
    postfix = ''
    tempStack = []
    formatted_regex = clean_regex(expression)
    print(formatted_regex)
    for char in formatted_regex:
        if char == '(':
            tempStack.append(char)
        elif char == ')':
            while tempStack[-1] != '(':
                postfix += tempStack.pop()
            tempStack.pop()
        # Operator
        else:
            while len(tempStack) > 0:
                top_char = tempStack[-1]
                current_char_precedence = get_precedence(char)
                top_char_precedence = get_precedence(top_char)
                if top_char_precedence >= current_char_precedence:
                    postfix += tempStack.pop()
                else:
                    break
            tempStack.append(char)
    while tempStack:
        # Processing the postfix
        postfix += tempStack.pop()
    return postfix


# We need to explicitly include '.' between concats
# This is needed to create valid postfix expressions for shunting yard
def clean_regex(expression):
    ans = ''
    # Both of the ones below can be extended to support many operation types (*/** etc)
    ops = set(['?', '#', '|', '@', '%'])
    bOps = set(['|', '%'])
    for i in range(len(expression)):
        char1 = expression[i]
        if i + 1 < len(expression):
            char2 = expression[i + 1]
            ans += char1
            if char1 != '(' and char2 != ')' and char2 not in ops and char1 not in bOps:
                ans += '%'
    ans += expression[-1]
    return ans


"""
    this is needed to create valid postfix expressions for shunting yard
    eg: 1 - (-2) creates a postfix of 1 2 - - which is invalid
    instead we convert to 1 0 2 - -
"""


def get_precedence(char):
    return PRECEDENCE.get(char, 6)


# Shunting Yard algorithm
class ShuntingYard:

    # Operator precedence dictionary
    PRECEDENCE = {'|': 1, '%': 1, '?': 2, '@': 2, '#': 2}
    OPERATORS = set(PRECEDENCE.keys())
    SYMBOLS = OPERATORS.union({'(', ')', EPSILON})

    def __init__(this):
        this.stack = Stack()
        this.output = []
        this.post_result = ""

    def concatenation(this, regex):
        reg_len = len(regex) - 1
        symbols = set(["(", "|", "?", "#", "%", "@", ")"])
        result = []
        for i in range(reg_len):
            result.append(regex[i])
            if regex[i] not in symbols and (regex[i+1] not in symbols or regex[i+1] == '('):
                result.append("%")
            else:
                case = {
                    regex[i] in {"@", "?", ")"} and regex[i+1] == "(": "%",
                    regex[i] in {"@", "?", "#", ")"} and regex[i+1] not in symbols: "%",
                }.get(True, "")
                result.append(case)
        result.append(regex[reg_len])
        return "".join(result)

    def revision(this, char):
        try:
            a = this.PRECEDENCE[char]
            b = this.PRECEDENCE[this.stack.peek()]
            return a <= b if a >= 0 and b >= 0 else False
        except KeyError:
            return False

    def to_postfix(this, regex):
        exp = this.concatenation(regex)
        for i in exp:
            if i.isalnum() or i == EPSILON:
                if this.stack.peek() in ("@", "#", "?"):
                    this.output.append(this.stack.pop())
                this.output.append(i)
            elif i == '(':
                this.stack.push(i)
            elif i == ')':
                while not this.stack.is_empty() and this.stack.peek() != '(':
                    a = this.stack.pop()
                    this.output.append(a)
                if this.stack.is_empty() or this.stack.peek() != '(':
                    return -1
                else:
                    this.stack.pop()
            else:
                while not this.stack.is_empty() and this.revision(i):
                    this.output.append(this.stack.pop())
                this.stack.push(i)
        while not this.stack.is_empty():
            this.output.append(this.stack.pop())
        this.post_result = "".join(this.output)
        return this.post_result
