# Thompson function
# https://userpages.umbc.edu/~squire/cs451_l6.html

'''
The thompson function takes a regular expression as input
and returns the start state of the resulting NFA.
It uses a vertexvertexvertexStack to keep track of sub-expressions,
and constructs the NFA incrementally as it processes each
symbolacter of the input string
'''
from collections import defaultdict
from re import S
import pandas as pd
from graphviz import Digraph
from machine import *
import pandas as pd

EPSILON = 'ε'


class Thompson():
    def __init__(this, regex=None, counter=None, automatas=None):
        this.transitionsList = []
        this.splitTransitionsList = []
        this.regex = regex
        this.finalStatesList = []
        vertexvertexvertexStack = []
        # Edge dictionary represents transitions to other states
        edgeDict = {}
        stateCount = 0
        this.states = []
        this.states_list = []
        this.startingState = None
        this.finalState = None
        this.symbolList = []
        this.error = False
        this.counter = counter
        this.automatas = automatas
        this.result = []

    def compile(this):
        vertexStack = []
        start = this.counter+1
        end = this.counter+2
        automata_counter_A = this.counter+1
        automata_counter_B = this.counter+1
        this.case_concurrence()
        symbolList = []
        regex = this.regex
        for char in regex:
            if this.item(char):
                if char not in symbolList:
                    symbolList.append(char)
        this.symbolList = sorted(symbolList)
        # Thompson algorithm
        for symbol in regex:
            # Left parenthesis management
            if symbol == "(":
                vertexStack.append(startingState)
                startingState = None
                finalState = None
            # Right (end) parenthesis management
            elif symbol == ")":
                finalState = vertexStack.pop()
                if not vertexStack:
                    startingState = None
                else:
                    startingState = vertexStack[-1]
            # If kleene
            # Kleene star, 4 nodes, 4 transitions
            # From q1 to qfinal, Epsilon
            elif symbol == '@':
                try:
                    '''
                    # Kleene star guide/template:
                    new_start = State(stateCount)
                    new_end = State(stateCount)
                    end_state.add_transition(EPSILON, start_state)
                    end_state.add_transition(EPSILON, new_end)
                    new_start.add_transition(EPSILON, start_state)
                    new_start.add_transition(EPSILON, new_end)
                    start_state = new_start
                    end_state = new_end
                    '''
                    node1, node2 = vertexStack.pop()
                    this.counter = this.counter+1
                    automata_counter_A = this.counter
                    if automata_counter_A not in this.states:
                        this.states.append(automata_counter_A)
                    this.counter = this.counter+1
                    automata_counter_B = this.counter
                    if automata_counter_B not in this.states:
                        this.states.append(automata_counter_B)
                    this.result.append({})
                    this.result.append({})
                    vertexStack.append(
                        [automata_counter_A, automata_counter_B])
                    if start == node1:
                        start = automata_counter_A
                    if end == node2:
                        end = automata_counter_B
                    this.splitTransitionsList.append([node2, EPSILON, node1])
                    this.splitTransitionsList.append(
                        [node2, EPSILON, automata_counter_B])
                    this.splitTransitionsList.append(
                        [automata_counter_A, EPSILON, node1])
                    this.splitTransitionsList.append(
                        [automata_counter_A, EPSILON, automata_counter_B])
                except:
                    this.error = True
                    print("\nKleene error.")
            # If OR
            elif symbol == "|":
                try:
                    '''
                    # OR guide/template:
                    new_start = State()
                    new_end = State()
                    new_start.add_transition(EPSILON, start_state)
                    new_start.add_transition(EPSILON, end_state)
                    start_state = new_start
                    end_state = new_end
                    '''
                    # Save states in variables
                    # Add transitions (OR: 4 transitions)
                    # Also add transitions to transition list
                    this.counter = this.counter+1
                    automata_counter_A = this.counter
                    if automata_counter_A not in this.states:
                        this.states.append(automata_counter_A)
                    this.counter = this.counter+1
                    automata_counter_B = this.counter
                    if automata_counter_B not in this.states:
                        this.states.append(automata_counter_B)
                    this.result.append({})
                    this.result.append({})

                    node11, node12 = vertexStack.pop()
                    node21, node22 = vertexStack.pop()
                    vertexStack.append(
                        [automata_counter_A, automata_counter_B])
                    if start == node11 or start == node21:
                        start = automata_counter_A
                    if end == node22 or end == node12:
                        end = automata_counter_B
                    this.splitTransitionsList.append(
                        [automata_counter_A, EPSILON, node21])
                    this.splitTransitionsList.append(
                        [automata_counter_A, EPSILON, node11])
                    this.splitTransitionsList.append(
                        [node12, EPSILON, automata_counter_B])
                    this.splitTransitionsList.append(
                        [node22, EPSILON, automata_counter_B])
                except:
                    this.error = True
                    print("\nOR error.")
            # if Concatenation
            elif symbol == '%':
                try:
                    '''
                    # Concatenation guide/template:
                    new_start = State()
                    new_end = State()
                    new_start.add_transition(EPSILON, start_state)
                    new_start.add_transition(EPSILON, end_state)
                    start_state = new_start
                    end_state = new_end
                    ---------------------------------
                    e2 = stack.pop()
                    e1 = stack.pop()
                    e1.accept = False
                    e1.edges[None] = [e2]
                    stack.append(e1)
                    stack.append(e2)s
                    '''
                    # Save states in variables
                    node11, node12 = vertexStack.pop()
                    node21, node22 = vertexStack.pop()
                    vertexStack.append([node21, node12])
                    if start == node11:
                        start = node21
                    if end == node22:
                        end = node12
                    this.splitTransitionsList.append([node22, EPSILON, node11])
                except:
                    this.error = True
                    print("\nConcatenation error.")
            # if Positive
            elif symbol == '#':
                try:
                    '''
                    # Union guide/template:
                    new_start = State()
                    new_end = State()
                    new_start.add_transition(EPSILON, start_state)
                    new_start.add_transition(EPSILON, end_state)
                    start_state = new_start
                    end_state = new_end
                    '''
                    # Save states in variables
                    # Add transitions (UNION: 3 transitions)
                    # Add transition to transition list
                    node1, node2 = vertexStack.pop()
                    this.counter = this.counter+1
                    automata_counter_A = this.counter
                    if automata_counter_A not in this.states:
                        this.states.append(automata_counter_A)
                    this.counter = this.counter+1
                    automata_counter_B = this.counter
                    if automata_counter_B not in this.states:
                        this.states.append(automata_counter_B)
                    vertexStack.append(
                        [automata_counter_A, automata_counter_B])
                    this.result[node2]['ε'] = (node1, automata_counter_B)
                    if start == node1:
                        start = automata_counter_A
                    if end == node2:
                        end = automata_counter_B
                    this.splitTransitionsList.append([node2, EPSILON, node1])
                    this.splitTransitionsList.append(
                        [node2, EPSILON, automata_counter_B])
                    this.splitTransitionsList.append(
                        [automata_counter_A, EPSILON, node1])
                except:
                    this.error = True
                    print("\n+ error.")
            # If concurrence
            elif symbol == "?":
                try:
                    '''
                    # Concurrence guide/template:
                    new_start = State(stateCount)
                    new_end = State(stateCount)
                    end_state.add_transition(EPSILON, start_state)
                    end_state.add_transition(EPSILON, new_end)
                    new_start.add_transition(EPSILON, start_state)
                    new_start.add_transition(EPSILON, new_end)
                    start_state = new_start
                    end_state = new_end
                    '''
                    # Save states in variables
                    # Add transitions (CONCURRENCE: 3 transitions)
                    # Add transition to transition list
                    this.counter = this.counter+1
                    automata_counter_A = this.counter
                    if automata_counter_A not in this.states:
                        this.states.append(automata_counter_A)
                    this.counter = this.counter+1
                    automata_counter_B = this.counter
                    if automata_counter_B not in this.states:
                        this.states.append(automata_counter_B)
                    this.result.append({})
                    this.result.append({})

                    node11, node12 = vertexStack.pop()
                    node21, node22 = vertexStack.pop()
                    vertexStack.append(
                        [automata_counter_A, automata_counter_B])
                    if start == node11 or start == node21:
                        start = automata_counter_A
                    if end == node22 or end == node12:
                        end = automata_counter_B
                    this.splitTransitionsList.append(
                        [automata_counter_A, EPSILON, node21])
                    this.splitTransitionsList.append(
                        [automata_counter_A, EPSILON, node11])
                    this.splitTransitionsList.append(
                        [node12, EPSILON, automata_counter_B])
                    this.splitTransitionsList.append(
                        [node22, EPSILON, automata_counter_B])
                except:
                    this.error = True
                    print("\nCONCURRENCE error.")
            else:
                this.counter = this.counter+1
                automata_counter_A = this.counter
                if automata_counter_A not in this.states:
                    this.states.append(automata_counter_A)
                this.counter = this.counter+1
                automata_counter_B = this.counter
                if automata_counter_B not in this.states:
                    this.states.append(automata_counter_B)
                this.result.append({})
                this.result.append({})
                vertexStack.append([automata_counter_A, automata_counter_B])
                this.splitTransitionsList.append(
                    [automata_counter_A, symbol, automata_counter_B])

        this.startingState = start
        this.finalStatesList.append(end)

        df = pd.DataFrame(this.result)
        string_afn = df.to_string()
        for symbol in range(len(this.splitTransitionsList)):
            this.transitionsList.append(
                "(" + str(this.splitTransitionsList[symbol][0]) + " - " + str(this.splitTransitionsList[symbol][1]) + " - " + str(this.splitTransitionsList[symbol][2]) + ")")
        this.transitionsList = ', '.join(this.transitionsList)

        for symbol in range(len(this.states)):
            if symbol == len(this.states)-1:
                finalStatesList = symbol
            this.states_list.append(str(this.states[symbol]))
        this.states_list = ", ".join(this.states_list)

        if this.error == False:
            pass
        else:
            print("\nInvalid format or regex.")

    def closure(this, states):
        listStates = list(states)
        stack = set(states)
        epsilon_transitionsCache = {}
        while stack:
            curr = stack.pop()
            epsilon_transitionsList = epsilon_transitionsCache.get(curr)
            if epsilon_transitionsList is None:
                epsilon_transitionsList = [
                    t[2] for t in this.splitTransitionsList if t[0] == curr and t[1] == EPSILON]
                epsilon_transitionsCache[curr] = epsilon_transitionsList
            for e in epsilon_transitionsList:
                if e not in stack:
                    listStates.append(e)
                    stack.add(e)
        return listStates

    def lex_automata(this, filename):
        this.counter += 1
        this.startingState = this.counter
        states_set = defaultdict(set)
        finalState_set = defaultdict(set)
        symbol_set = defaultdict(set)
        for automata in this.automatas:
            this.finalStatesList.append(automata.finalStatesList[0])
            this.splitTransitionsList.extend(automata.splitTransitionsList)
            this.states.extend(automata.states)
            this.splitTransitionsList.append(
                [this.startingState, EPSILON, automata.startingState])

        # This will create a graph with nodes and edges,
        #  with labels indicating the direction of the edges.
        '''
        dot = Digraph()
        for state in this.states:
            if state in this.finalStatesList:
                dot.node(str(state), shape="doublecircle")
            else:
                dot.node(str(state), shape="circle")
        for transition in this.splitTransitionsList:
            if transition[1] == EPSILON:
                dot.edge(str(transition[0]), str(transition[2]), label=EPSILON)
            else:
                dot.edge(str(transition[0]), str(
                    transition[2]), label=transition[1])
        dot.render(filename, format='png', view=True)
        '''
    def item(this, char):
        if char.isalpha() or char.isnumeric() or char == '*' or char == '-' or char == EPSILON or char == '^' or char == ',' or char == '=' or char == '.' or char == '+' or char == '"':
            return True
        else:
            return False

    def case_concurrence(this):
        this.regex = this.regex.replace('?', 'ε?')

    def string(this, string):
        currStates = this.closure([this.startingState])
        for symbol in string:
            newStates = {trans[2] for state in currStates
                         for trans in this.splitTransitionsList
                         if state == trans[0] and symbol == trans[1]}
            if not newStates:
                return False
            currStates = this.closure(newStates)
        finStates = this.closure(currStates)
        if isinstance(this.finalStatesList, list):
            for fs in this.finalStatesList:
                if fs in finStates:
                    return (True, fs)
            return False
        else:
            return this.finalStatesList in finStates
