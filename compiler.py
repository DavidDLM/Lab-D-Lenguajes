'''
Pickle:
If you do not have any interoperability requirements (e.g. you are 
just going to use the data with Python) and a binary format is fine, 
go with cPickle which gives you really fast Python object serialization.

'''

import pickle
import re
from machine import *
from postfix import *
from thompson import Thompson

COMMENTS = '''
# Language classifier
'''
HEADER = '''
import re
import pickle
'''
CONTENT = '''

def load_pickle(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)


def get_token_types(text, final_elements, automata_elements):
    result = []
    regex = re.compile(r'"[^"]*"|\S+')
    result = regex.findall(text)

    token_types = []
    for char in result:
        char = char.replace(' ', ',')
        #print(char)
        belongs = final_elements.string(char)
        try:
            if belongs == False:
                token_types.append(char + " : Unknown")
            elif belongs[0]:
                for elem in automata_elements:
                    if belongs[1] in elem[1].finalStatesList:
                        token_types.append(
                            char + " : " + str(elem[0][0]).upper())
                        break
        except Exception:
            pass
    return token_types


def write_output_file(text, token_types, file_path):
    with open(file_path, 'w') as f:
        f.write(text)
        f.write('\\n\\n')
        for result in token_types:
            f.write(result)
            f.write('\\n')


if __name__ == "__main__":
    automata_elements = load_pickle('automataElements.pkl')
    final_elements = load_pickle('finalElements.pkl')

    with open('./domain/dom1.txt', 'r') as f:
        body = f.read()

    token_types = get_token_types(body, final_elements, automata_elements)
    write_output_file(body, token_types, "language.txt")
'''


class TokenCompiler:
    def __init__(this, filename):
        this.filename = filename

    def compileTokens(this, output_file):
        automatas = []
        joinTokens = []
        individualNFA = []
        token_nfa_map = {}
        counter = -1
        fileTokens = Tokens()
        fileTokens.tokenize(this.filename)

        # Combine tokens that are substrings of other tokens
        for i in range(len(fileTokens.tokens)):
            for j in range(len(fileTokens.tokens)):
                if i != j and fileTokens.tokens[i][0] in fileTokens.tokens[j][1]:
                    fileTokens.tokens[i] = (
                        fileTokens.tokens[i][0], fileTokens.tokens[i][1], True)
                    break
                else:
                    fileTokens.tokens[i] = (
                        fileTokens.tokens[i][0], fileTokens.tokens[i][1], False)

        # Generate individual NFAs for each token
        for token in fileTokens.tokens:
            if token[2]:
                #postfix = shunting_yard(token[1])
                conversion = ShuntingYard()
                conversion.to_postfix(token[1])
                postfix = conversion.post_result
                tokenNFA = Thompson(regex=postfix, counter=counter)
                tokenNFA.compile()
                counter = tokenNFA.counter
                automatas.append((token, tokenNFA))

        # Join tokens with regular expressions
        # Use joinTokens = []
        for token in fileTokens.tokens:
            if token[2]:
                joinTokens.append((token[0], token[1], token[2]))
            if not token[2]:
                operators = []
                regex_splitted = re.findall('\w+|[?()|\-=@#%+*"]', token[1])
                operators.extend(regex_splitted)
                for i, element in enumerate(operators):
                    '''
                    if element in token_nfa_map:
                        operators[i] = "("+token_nfa_map[element].regex+")"
                    new_regex = ''.join(operators)
                    join_tokens.append(new_regex)
                    '''
                    for tokenNFA in automatas:
                        if element == tokenNFA[0][0]:
                            operators[i] = "("+tokenNFA[0][1]+")"
                result = ''.join(operators)

                joinTokens.append((token[0], result, token[2]))

        # Generate NFAs for joined tokens
        for token in joinTokens:
            if not token[2]:
                #postfix = shunting_yard(token[1])
                conversion = ShuntingYard()
                conversion.to_postfix(token[1])
                postfix = conversion.post_result
                tokenNFA = Thompson(regex=postfix, counter=counter)
                tokenNFA.compile()
                counter = tokenNFA.counter
                automatas.append((token, tokenNFA))

        # NFA list
        individualNFA = [tokenNFA for _,
                         tokenNFA in automatas if tokenNFA is not None]

        finalNFA = Thompson(counter=counter, automatas=individualNFA)
        finalNFA.lex_automata(output_file)

        # Serialize data using pickle
        with open('automataElements.pkl', 'wb') as f:
            pickle.dump(automatas, f)
        with open('finalElements.pkl', 'wb') as f:
            pickle.dump(finalNFA, f)

        with open('lexer.py', 'w') as file:
            file.write(COMMENTS)
            file.write(HEADER)
            file.write(CONTENT)
