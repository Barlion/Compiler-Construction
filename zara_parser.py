class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_index = 0

    def parse(self):
        return self._parse_statements()

    def _parse_statements(self):
        statements = []
        while self.current_index < len(self.tokens):
            token = self._current_token()

            # Stop parsing when we reach a closing brace
            if token.type == 'RBRACE':
                break

            statement = self._parse_statement()
            if statement is not None:
                statements.append(statement)
        return statements

    def _parse_statement(self):
        token = self._current_token()

        print(f"Parsing token: {token.type}")

        if token.type == 'EOF':
            return None  # End of file or end of input
        elif token.type == 'IF':
            return self._parse_if()  # Handle if statement
        elif token.type == 'IDENTIFIER':
            return self._parse_assignment()  # Handle assignment for identifiers
        else:
            raise SyntaxError(f"Unexpected token: {token.type}")

    def _parse_if(self):
        # Start parsing the 'if' statement
        print("Parsing if statement...")
        self._consume('IF')  # Consume the 'if' keyword
        self._consume('LPAREN')  # Consume '(' for condition
        condition = self._parse_expression()  # Parse the condition
        self._consume('RPAREN')  # Consume ')' after condition
        self._consume('LBRACE')  # Consume '{' for the body
        body = self._parse_statements()  # Parse the body of the if statement
        self._consume('RBRACE')  # Consume '}' after the block
        return ('if', condition, body)

    def _parse_assignment(self):
        # Start parsing an assignment
        print("Parsing assignment...")
        identifier = self._consume('IDENTIFIER')  # Consume the variable name
        self._consume('ASSIGN')  # Expect '=' for assignment
        expression = self._parse_expression()  # Parse the expression on the right-hand side
        self._consume('SEMICOLON')  # Expect ';' at the end
        return ('assign', identifier, expression)

    def _parse_expression(self):
        # Expressions can be simple values or more complex terms
        left = self._parse_term()
        while self._current_token().type in ['GT', 'LT', 'PLUS', 'MINUS']:
            operator = self._consume(self._current_token().type)  # Consume the operator
            right = self._parse_term()  # Parse the right side
            left = (operator, left, right)  # Construct an expression tree
        return left

    def _parse_term(self):
        # Terms can be identifiers or numbers
        token = self._current_token()
        if token.type == 'IDENTIFIER':
            return self._consume('IDENTIFIER')
        elif token.type == 'NUMBER':
            return self._consume('NUMBER')
        else:
            raise SyntaxError(f"Unexpected token in term: {token.type}")

    def _current_token(self):
        return self.tokens[self.current_index]

    def _consume(self, token_type):
        token = self._current_token()
        print(f"Consuming token: {token.type}")
        if token.type == token_type:
            self.current_index += 1
            return token
        else:
            raise SyntaxError(f"Expected {token_type} but got {token.type}")

# Example usage of the parser
if __name__ == "__main__":
    from tokenizer import Tokenizer

    # Example source code
    source_code = "if (x > 5) { x = x - 1; }"
    tokenizer = Tokenizer(source_code)
    tokens = tokenizer.tokenize()

    # Create a parser object
    parser = Parser(tokens)
    try:
        # Parse the token stream and print the result
        parsed = parser.parse()
        print(parsed)
    except SyntaxError as e:
        print(f"Error: {e}")
