import operator as op

###
# Custom types for Lisp
class LispType(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value

class Symbol(LispType):
    pass

class String(LispType):
    pass
###

functions = {
    '+': op.add,
    '-': op.sub,
    '*': op.mul,
    '/': op.truediv,
}
def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            if token in functions:
                return Symbol(token)
            else:
                return String(token)

###
# Tokenize and parse the lisp input
def tokenize(string):
    if len(string) == 0:
        raise SyntaxError("input is empty, terminate")
    return string.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(tokens):
    token = tokens.pop(0)

    if token == '(':
        token_list = []
        while tokens[0] != ')':
            token_list.append(parse(tokens))
        tokens.pop(0)

        return token_list
    elif token == ')':
        raise SyntaxError("Unexpected ')' in tokenized list")
    else:
        return atom(token)
###


###
# evaluate the parsed lisp program
def eval(program, funcs=functions):
    if isinstance(program, int):
        return program
    elif isinstance(program, float):
        return program
    elif isinstance(program, String):
        return program
    elif isinstance(program, Symbol):
        try:
            return funcs[program.value]
        except KeyError:
            raise TypeError("Function: {} not in language spec".format(program))
    else:
        func = eval(program[-1], funcs)
        args = [eval(arg, funcs) for arg in program[:-1]]
        return func(*args)
###

def main():
    while True:
        input_string = input('>>> ')
        input_string_parsed = parse(tokenize(input_string))
        if input_string_parsed is not None:
            print("parsed: {}".format(input_string_parsed))
            value = eval(input_string_parsed)
            print("{0} #=> {1}".format(input_string, value))

if __name__ == '__main__':
    main()

