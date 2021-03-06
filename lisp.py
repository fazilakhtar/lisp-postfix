import operator as op
import copy


def consFunc(*args):
    (y, x) = args
    if isinstance(x, list):
        if isinstance(y, list):
            return x + y
        else:
            return x + [y]
    else:
        if isinstance(y, list):
            return [x] + y
        else:
            return [x] + [y]

def atomFunc(*args):
    if isinstance(args[0], str):
        if "'" in args[0]:
            return False
    else:
        return not isinstance(args[0], Symbol)

functions = {
    '+': op.add,
    '-': op.sub,
    '*': op.mul,
    '/': op.truediv,
    'eq?': op.is_,
    'cons': consFunc,
    'car': lambda x : x.pop(),
    'cdr': lambda x : x[:-1],
    'atom?': atomFunc,
}

###
# Custom types for Lisp
class Symbol(str):
    pass

class List(list):
    pass

class Lambda:
    def __init__(self, args, expression, funcs):
        self.args = args
        self.expression = expression
        self.funcs = funcs

    def __call__(self, *expression):
        # functions.update(dict(zip(self.args, expression)))
        ## copy 'funcs' into a local state
        local_funcs = copy.deepcopy(functions)
        local_funcs.update(dict(zip(self.args, expression)))
        return eval(self.expression, local_funcs)
###

# convert expression to postfix lisp
def lispStringUnchanged(expr):
    if isinstance(expr, list):
        return '(' + ' '.join(map(lispStringUnchanged, expr)) + ')'
    else:
        return str(expr)

def lispString(expr):
    if isinstance(expr, list):
        return List(expr)
    else:
        s = str(expr)
        if s[-1] == "'":
            return s
        else:
            return s + "'"

def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


###
# Tokenize and parse the lisp input
def tokenize(string):
    if len(string) == 0:
        raise SyntaxError("input is empty, terminate")
    string = string.replace('(', ' ( ').replace(')', ' ) ')
    string = string.replace("'", " ' ").split()
    return string

def parse(tokens):
    token = tokens.pop()
    
    if token == ')':
        token_list = []
        while tokens[-1] != '(':
            token_list.append(parse(tokens))
        tokens.pop()

        return token_list
    elif token == "'":
        token_list = []
        if len(tokens) >= 1:
            while tokens[-1] != "(":
                token_list.append(parse(tokens))
            return lispString(token_list[0])
    elif token == '(':
        raise SyntaxError("Unexpected '(' in tokenized list")
    else:
        return atom(token)
###


###
# evaluate the parsed lisp program
def eval(program, funcs=functions):
    # print("in-eval: ", program)
    # print("funcs: ", funcs)
    if isinstance(program, int):
        return program
    elif isinstance(program, float):
        return program
    elif program[0] == 'quote':
        return lispStringUnchanged(program[1]) + "'"
    elif program[0] == 'define':
        name = program[1]
        value = eval(program[2], funcs)
        funcs[name] = value
    elif program[0] == 'lambda':
        args = program[1]
        expression = program[2]
        return Lambda(args, expression, funcs)
    elif program[0] == 'cond':
        clauses = program[1]
        for clause in clauses:
            if clause[-1] == 'else':
                if not isinstance(clause[0], Symbol):
                    return eval(clause[0], funcs)
                else:
                    return clause[0]
            else:
                if eval(clause[1], funcs):
                    return clause[0]
    elif isinstance(program, Symbol):
        return funcs[program]
    elif isinstance(program, List):
        return program
    elif not isinstance(program, list):
        return program
    else:
        func = eval(program[0], funcs)
        args = [eval(arg, funcs) for arg in program[1:]]
        return func(*args)
###

def main():
    while True:
        input_string = input('>>> ')
        input_string_parsed = parse(tokenize(input_string))
        # print("parsed: ", input_string_parsed)
        if input_string_parsed is not None:
            value = eval(input_string_parsed)
            print("{0} #=> {1}".format(input_string, value))


if __name__ == '__main__':
    main()

