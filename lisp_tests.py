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
        self.assertEqual(eval(parse(tokenize('(5 1 -)'))), 4)
        self.assertEqual(eval(parse(tokenize('((10 5 -) 1 -)'))), 4)
        self.assertEqual(eval(parse(tokenize('((10.0 5.0 -) 1.0 -)'))), 4.0)

    def test_multiplication(self):
        self.assertEqual(eval(parse(tokenize('(2 2 *)'))), 4)
        self.assertEqual(eval(parse(tokenize('((5 5 *) 0 *)'))), 0)
        self.assertEqual(eval(parse(tokenize('((5.0 5.0 *) 0.0 *)'))), 0.0)

    def test_division(self):
        self.assertEqual(eval(parse(tokenize('(10 5 /)'))), 2.0)
        self.assertEqual(eval(parse(tokenize('(10 1 /)'))), 10.0)
        self.assertEqual(eval(parse(tokenize('(10.0 1.0 /)'))), 10.0)
        with self.assertRaises(ZeroDivisionError):
            eval(parse(tokenize('(10 0 /)')))

    def test_outOfScope(self):
        with self.assertRaises(TypeError):
            eval(parse(tokenize('(2 2 %)')))

    def test_eq(self):
        self.assertEqual(eval(parse(tokenize('(1 1 eq?)'))), True)
        self.assertEqual(eval(parse(tokenize('(1 2 eq?)'))), False)

    def test_quote(self):
        self.assertEqual(eval(parse(tokenize('(a quote)'))), "a'")
        self.assertEqual(eval(parse(tokenize('((1 2 +) quote)'))), "(1 2 +)'")
        self.assertEqual(eval(parse(tokenize("((1 2 3)'' quote)"))), "(1 2 3)'")

    def test_cons(self):
        self.assertEqual(eval(parse(tokenize('(3 4 cons)'))), [3, 4])
        self.assertEqual(eval(parse(tokenize('((3 4) 10 cons)'))), [3, 4, 10])
        self.assertEqual(eval(parse(tokenize('(10 (3 4) cons)'))), [10, 3, 4])

if __name__ == '__main__':
    unittest.main()

