from queue import LifoQueue  # For stack operations
import re


# Machine class
class Machine:
    def __init__(this, initialState, finalState):
        this.initialState = initialState
        this.finalState = finalState

    def getFinalMachineState(this):
        return this.finalState

    def getInitialMachineState(this):
        return this.initialState

    def display():
        return


# State class
class State:

    def __init__(this, state_id):
        this.state_id = state_id

    def __repr__(this):
        return str(this.state_id)


# Transitions class
class Transitions:
    def __init__(this, initialState, finalState, symbol):
        this.initialState = initialState
        this.finalState = finalState
        this.symbol = symbol

    def getInitialTransitionState(this):
        return this.initialState

    def setInitialTransitionState(this, initialState):
        this.initialState = initialState

    def getFinalTransitionState(this):
        return this.finalState

    def setFinalTransitionState(this, finalState):
        this.finalState = finalState

    def getTransitionSymbol(this):
        return this.symbol


# Clase Node based in a node from Linked List
# https://www.tutorialspoint.com/python_data_structure/python_linked_lists.htm
class Node(object):
    # Node class with parents, right node, left node, symbols
    def __init__(this, symbol, parent, prev, next):
        this.symbol = symbol
        this.parent = parent
        this.prev = prev
        this.next = next
        this.nullable = False
        this.firstpos = []
        this.lastpos = []
        this.followpos = []
        this.pos = None


# Stack class with stack functions
# Import LastInFirstOut
# https://codefather.tech/blog/create-stack-python/#:~:text=To%20create%20a%20stack%20in%20Python%20you%20can%20use%20a,the%20top%20of%20the%20stack.
class Stack:
    def __init__(this):
        this.stack = []

    def is_empty(this):
        return not this.stack

    def peek(this):
        return this.stack[-1] if not this.is_empty() else "$"

    def pop(this):
        return this.stack.pop() if not this.is_empty() else "$"

    def push(this, op):
        this.stack.append(op)


# Tokens class
class Tokens():
    def __init__(this):
        this.tokens = []

    # Regex defined as bucle
    def tokenize(this, file):
        with open(file, 'r') as f:
            archiveLines = f.read()
        variables = re.findall(r'\s*(\w+)\s*{', archiveLines)
        tokenStrip = r'let\s+([a-zA-Z0-9_-]+)\s+=\s+(.*)'
        for line in archiveLines.splitlines():
            match = re.match(tokenStrip, line.strip())
            if match and match.group(1) in variables:
                this.tokens.append((match.group(1), match.group(2)))
        return this.tokens
