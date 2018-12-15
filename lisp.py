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

# convert expression to postfix lisp
def lispString(expr):
    if isinstance(expr, list):
        return '(' + ' '.join(map(lispString, expr)) + ')'
    else:
        return str(expr)

def quoteFunc(*args):
    if len(args) == 1:
        return "'{}".format(lispString(args[0]))
    else:
        return "'{}".format(lispString(args[1]))

functions = {
    '+': op.add,
    '-': op.sub,
    '*': op.mul,
    '/': op.truediv,
    'eq?': op.is_,
    'quote': quoteFunc,
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
                if token == "'":
                    return token
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
    # print("program: {}".format(program))
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
        if func == quoteFunc:
            args = [arg for arg in program[:-1]]
        else:
            args = [eval(arg, funcs) for arg in program[:-1]]
        return func(*args)
###

def main():
    while True:
        input_string = input('>>> ')
        print("tokenized: ", tokenize(input_string))
        input_string_parsed = parse(tokenize(input_string))
        if input_string_parsed is not None:
            # print("parsed: {}".format(input_string_parsed))
            value = eval(input_string_parsed)
            print("{0} #=> {1}".format(input_string, value))

if __name__ == '__main__':
    main()

