import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"{self.type}: {self.value}"

class Tokenizer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.token_specification = [
            ('NUMBER',    r'\d+'),           # Integer
            ('IF',        r'\bif\b'),        # 'if' keyword
            ('ELSE',      r'\belse\b'),      # 'else' keyword
            ('IDENTIFIER', r'[a-zA-Z_]\w*'),  # Identifiers
            ('ASSIGN',     r'='),             # Assignment operator
            ('PLUS',       r'\+'),            # Addition operator
            ('MINUS',      r'-'),             # Subtraction operator
            ('GT',         r'>'),             # Greater than
            ('LT',         r'<'),             # Less than
            ('LPAREN',     r'\('),            # Left Parenthesis
            ('RPAREN',     r'\)'),            # Right Parenthesis
            ('LBRACE',     r'\{'),            # Left Brace
            ('RBRACE',     r'\}'),            # Right Brace
            ('SEMICOLON',  r';'),             # Statement terminator
            ('SKIP',       r'[ \t]+'),        # Skip spaces and tabs
            ('MISMATCH',   r'.'),             # Any unmatched character
        ]
        self.token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.token_specification)

    def tokenize(self):
        for match in re.finditer(self.token_regex, self.source_code):
            token_type = match.lastgroup
            token_value = match.group(token_type)
            if token_type == 'SKIP':
                continue
            elif token_type == 'MISMATCH':
                raise SyntaxError(f'Unexpected character: {token_value}')
            else:
                self.tokens.append(Token(token_type, token_value))
        return self.tokens

# Example usage
if __name__ == "__main__":
    source_code = "if (x > 5) { x = x - 1; }"
    tokenizer = Tokenizer(source_code)
    tokens = tokenizer.tokenize()
    print(tokens)
