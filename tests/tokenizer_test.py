# tests/test_tokenizer.py
import unittest
from tokenizer import Tokenizer

class TestTokenizer(unittest.TestCase):
    def test_tokenizer_basic(self):
        code = 'if (x > 5) { x = x - 1; }'
        tokenizer = Tokenizer(code)
        tokens = tokenizer.tokenize()
        expected_types = ['IF', 'LPAREN', 'IDENTIFIER', 'GT', 'NUMBER', 'RPAREN', 'LBRACE', 'IDENTIFIER', 'ASSIGN', 'IDENTIFIER', 'MINUS', 'NUMBER', 'SEMICOLON', 'RBRACE']
        token_types = [token.type for token in tokens]
        self.assertEqual(token_types, expected_types)

if __name__ == '__main__':
    unittest.main()
