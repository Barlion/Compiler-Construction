# tests/test_parser.py
import unittest
from zara_parser import Parser
from tokenizer import Tokenizer

class TestParser(unittest.TestCase):
    def test_if_statement(self):
        code = 'if (x > 5) { x = x - 1; }'
        tokenizer = Tokenizer(code)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens)
        parsed = parser.parse()
        expected = [('IF', ('GT', 'x', '5'), [('ASSIGN', 'x', ('MINUS', 'x', '1'))])]
        self.assertEqual(parsed, expected)

if __name__ == '__main__':
    unittest.main()
