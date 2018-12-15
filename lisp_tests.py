import unittest
from lisp import *

class ListTests(unittest.TestCase):

    def test_tokenize(self):
        with self.assertRaises(SyntaxError):
            tokenize('')
        self.assertEqual(tokenize('(2 2 +)'), ['(', '2', '2', '+', ')'])
        self.assertEqual(
            tokenize('((2 2 +) 4 +)'), 
            ['(', '(', '2', '2', '+', ')', '4', '+', ')']
        )

    def test_parse(self):
        # self.assertEqual(parse(tokenize('(2 2 +)')), [2, 2, +])
        # self.assertEqual(parse(tokenize('(( 2 2 +) 4 +')), [[2, 2, +], 4, +])

if __name__ == '__main__':
    unittest.main()

