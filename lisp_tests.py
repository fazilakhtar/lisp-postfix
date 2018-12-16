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

    # def test_outOfScope(self):
    #     with self.assertRaises(TypeError):
    #         eval(parse(tokenize('(2 2 %)')))

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
        self.assertEqual(eval(parse(tokenize("(a' quote)"))), "a'")
        self.assertEqual(eval(parse(tokenize('((1 2 +) quote)'))), "(+ 2 1)")
        self.assertEqual(eval(parse(tokenize("((1 2 3) quote)"))), "(3 2 1)")
        self.assertEqual(eval(parse(tokenize("((1 2 3)' quote)"))), "(3 2 1)'")

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

    def test_atom(self):
        self.assertEqual(eval(parse(tokenize('(3 atom?)'))), True)
        self.assertEqual(eval(parse(tokenize("(3' atom?)"))), False)
        self.assertEqual(eval(parse(tokenize("((3 2 1)' atom?)"))), False)

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
            eval(parse(tokenize('((((c 1 eq?) one) ((c 2 eq?) two) '\
                '((c 3 eq?) three) (else no-idea)) cond)'))),
            'three'
        )
        self.assertEqual(
            eval(parse(tokenize('((((c 1 eq?) one) ((c 2 eq?) two) '\
                '((c 6 eq?) three) (else no-idea)) cond)'))),
            'no-idea'
        )



if __name__ == '__main__':
    unittest.main()

