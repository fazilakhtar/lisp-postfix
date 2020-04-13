import unittest
from lisp import *

class ListTests(unittest.TestCase):

    token = '+'
    plus = Symbol(token)
    # print(plus)

    def test_tokenize(self):
        with self.assertRaises(SyntaxError):
            tokenize('')
        self.assertEqual(tokenize('(2 2 +)'), ['(', '2', '2', '+', ')'])
        self.assertEqual(
            tokenize('((2 2 +) 4 +)'), 
            ['(', '(', '2', '2', '+', ')', '4', '+', ')']
        )

    def test_parse(self):
        plus = Symbol('+')
        minus = Symbol('-')
        self.assertTrue(parse(tokenize('(2 2 +)')), [2, 2, plus])
        self.assertTrue(
            parse(tokenize('(( 2 2 +) 4 +)')), 
            [[2, 2, plus], 4, plus]
        )
        self.assertTrue(parse(tokenize('(50 5 -)')), [50, 5, minus])

    ## Tests for 'Normal Form'
    def test_addition(self):
        self.assertEqual(eval(parse(tokenize('(2 2 +)'))), 4)
        self.assertEqual(eval(parse(tokenize('((4 3 +) 4 +)'))), 11)
        self.assertEqual(eval(parse(tokenize('((4.0 3.0 +) 4.0 +)'))), 11.0)

    def test_subtraction(self):
        self.assertEqual(eval(parse(tokenize('(1 5 -)'))), 4)
        self.assertEqual(eval(parse(tokenize('((5 10 -) 1 -)'))), -4)
        self.assertEqual(eval(parse(tokenize('((10.0 5.0 -) 1.0 -)'))), 6.0)

    def test_multiplication(self):
        self.assertEqual(eval(parse(tokenize('(2 2 *)'))), 4)
        self.assertEqual(eval(parse(tokenize('((5 5 *) 0 *)'))), 0)
        self.assertEqual(eval(parse(tokenize('((5.0 5.0 *) 0.0 *)'))), 0.0)

    def test_division(self):
        self.assertEqual(eval(parse(tokenize('(5 10 /)'))), 2.0)
        self.assertEqual(eval(parse(tokenize('(10 1 /)'))), 0.1)
        self.assertEqual(eval(parse(tokenize('(1.0 10.0 /)'))), 10.0)
        with self.assertRaises(ZeroDivisionError):
            eval(parse(tokenize('(0 10 /)')))

    def test_eq(self):
        self.assertEqual(eval(parse(tokenize('(1 1 eq?)'))), True)
        self.assertEqual(eval(parse(tokenize('(1 2 eq?)'))), False)
        self.assertEqual(
            eval(parse(tokenize('((2 10 +) (3 4 *) eq?)'))), 
            True
        )
        self.assertEqual(
            eval(parse(tokenize('((2 4 +) 5 eq?)'))), 
            False
        )

    def test_quote(self):
        self.assertEqual(eval(parse(tokenize("(a' quote)"))), "a''")
        self.assertEqual(eval(parse(tokenize('((1 2 +) quote)'))), "(+ 2 1)'")
        self.assertEqual(eval(parse(tokenize("((1 2 3) quote)"))), "(3 2 1)'")
        # self.assertEqual(eval(parse(tokenize("((1 2 3)' quote)"))), "(3 2 1)'")

    def test_cons(self):
        self.assertEqual(eval(parse(tokenize('(3 4 cons)'))), [3, 4])
        self.assertEqual(eval(parse(tokenize('((3 4 +) 10 cons)'))), [7, 10])
        self.assertEqual(eval(parse(tokenize('(10 (3 4 *) cons)'))), [10, 12])
        self.assertEqual(
            eval(parse(tokenize('((3 4 cons) (5 6 cons) cons)'))),
            [3, 4, 5, 6]
        )

    def test_car(self):
        self.assertEqual(eval(parse(tokenize('((3 4 cons) car)'))), 4)
        self.assertEqual(eval(parse(tokenize('((3 (5 2 cons) cons) car)'))), 2)

    def test_cdr(self):
        self.assertEqual(eval(parse(tokenize('((3 4 cons) cdr)'))), [3])
        self.assertEqual(
            eval(parse(tokenize('((3 (5 2 cons) cons) cdr)'))), 
            [3, 5]
        )
        eval(parse(tokenize("((1 2 3)' sl define)")))
        self.assertEqual(eval(parse(tokenize('(((sl cdr) cdr) cdr)'))), [])
        self.assertEqual(eval(parse(tokenize('((sl cdr) cdr)'))), [3])

    def test_atom(self):
        self.assertEqual(eval(parse(tokenize('(3 atom?)'))), True)
        self.assertEqual(eval(parse(tokenize("(3' atom?)"))), False)
        self.assertEqual(eval(parse(tokenize("((3 2 1)' atom?)"))), True)

    def test_define(self):
        eval(parse(tokenize('(5 a define)')))
        self.assertEqual(functions['a'], 5)
        self.assertEqual(eval(parse(tokenize('(a 5 +)'))), 10)
        self.assertEqual(eval(parse(tokenize('(a 10 *)'))), 50)

    def test_lambda(self):
        eval(parse(tokenize('(((x x *) x lambda) square define)')))
        self.assertEqual(eval(parse(tokenize('(5 square)'))), 25)
        self.assertEqual(eval(parse(tokenize('(0 square)'))), 0)
        self.assertEqual(eval(parse(tokenize('(5.5 square)'))), 30.25)

    def test_cond(self):
        eval(parse(tokenize('(3 c define)')))
        self.assertEqual(
            eval(parse(tokenize('(((else no-idea) ((c 3 eq?) three) '\
                '((c 2 eq?) two) ((c 1 eq?) one)) cond)'))),
            'three'
        )
        self.assertEqual(
            eval(parse(tokenize('(((else no-idea) ((c 6 eq?) three) '\
                '((c 2 eq?) two) ((c 1 eq?) one)) cond)'))),
            'no-idea'
        )

    def test_fib(self):
        # def fib(n):
        #     if n<0:
        #         raise
        #     elif n==0:
        #         return 0
        #     elif n==1:
        #         return 1
        #     else:
        #         return fib(n-1)+fib(n-2)
        #
        # Prefix Lisp
        # (define fib (lambda n (cond ((0 (eq? n 0)) (1 (eq? n 1) (else ((+ (fib (- n 1)) (fib (- n 2))))))))))
        #
        # Postfix Lisp
        # (((((else (((2 n -) fib) ((1 n -) fib) +)) ((1 n eq?) 1) ((0 n eq?) 0)) cond) n lambda) fib define)
        eval(parse(tokenize('(((((else (((2 n -) fib) ((1 n -) fib) +)) ((1 n eq?) 1) ((0 n eq?) 0)) cond) n lambda) fib define)')))
        self.assertEqual(eval(parse(tokenize('(0 fib)'))), 0)
        self.assertEqual(eval(parse(tokenize('(19 fib)'))), 4181)
        # self.assertEqual(eval(parse(tokenize('(20 fib)'))), 6765)



if __name__ == '__main__':
    unittest.main()

