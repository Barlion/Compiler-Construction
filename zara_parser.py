class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"{self.type}: {self.value}"

class Tokenizer:
    def __init__(self, code):
        self.tokens = []
        self.position = 0
        self.tokenize(code)

    def tokenize(self, code):
        i = 0
        while i < len(code):
            char = code[i]
            if char.isspace():
                i += 1
            elif char.isalpha():
                start = i
                while i < len(code) and code[i].isalnum():
                    i += 1
                value = code[start:i]
                if value == "if":
                    self.tokens.append(Token("IF", value))
                else:
                    self.tokens.append(Token("IDENTIFIER", value))
            elif char.isdigit():
                start = i
                while i < len(code) and code[i].isdigit():
                    i += 1
                value = code[start:i]
                self.tokens.append(Token("NUMBER", value))
            elif char == '>':
                self.tokens.append(Token("GT", char))
                i += 1
            elif char == '=':
                self.tokens.append(Token("ASSIGN", char))
                i += 1
            elif char == '-':
                self.tokens.append(Token("MINUS", char))
                i += 1
            elif char == '(':
                self.tokens.append(Token("LPAREN", char))
                i += 1
            elif char == ')':
                self.tokens.append(Token("RPAREN", char))
                i += 1
            elif char == '{':
                self.tokens.append(Token("LBRACE", char))
                i += 1
            elif char == '}':
                self.tokens.append(Token("RBRACE", char))
                i += 1
            elif char == ';':
                self.tokens.append(Token("SEMICOLON", char))
                i += 1

    def next_token(self):
        if self.position < len(self.tokens):
            token = self.tokens[self.position]
            self.position += 1
            return token
        return None

    def peek_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = self.tokens.next_token()
        self.temp_count = 1
        self.intermediate_code = []
        self.parse()

    def parse(self):
        if self.current_token and self.current_token.type == "IF":
            print("Parsing if statement...")
            self._parse_if()

    def _parse_if(self):
        self._consume("IF")
        self._consume("LPAREN")
        left = self._consume("IDENTIFIER")
        op = self._consume("GT")
        right = self._consume("NUMBER")
        self._consume("RPAREN")
        temp_condition = self._new_temp()
        self.intermediate_code.append(f"{temp_condition} = {left.value} {op.value} {right.value}")
        self._consume("LBRACE")
        body = self._parse_body()
        self._consume("RBRACE")

        # Adding labels for branching
        label_true = self._new_label()
        label_false = self._new_label()
        self.intermediate_code.append(f"IF {temp_condition} GOTO {label_true}")
        self.intermediate_code.append(f"GOTO {label_false}")
        self.intermediate_code.append(f"{label_true}:")

        # Add parsed body to intermediate code, with fix for tuple format
        for stmt in body:
            if isinstance(stmt, tuple) and stmt[0] == 'assign':
                self.intermediate_code.append(f"{stmt[1]} = {stmt[2]}")
            else:
                self.intermediate_code.append(stmt)

        self.intermediate_code.append(f"{label_false}:")

        print("Parsed:", [('if', temp_condition, body)])
        print("Intermediate Code:")
        for line in self.intermediate_code:
            print(line)

    def _parse_body(self):
        body = []
        if self.current_token.type == "IDENTIFIER":
            print("Parsing assignment...")
            assignment = self._parse_assignment()
            body.append(assignment)
        return body

    def _parse_assignment(self):
        left = self._consume("IDENTIFIER")
        assign_op = self._consume("ASSIGN")
        right = self._consume("IDENTIFIER")
        operator = self._consume("MINUS")
        value = self._consume("NUMBER")
        self._consume("SEMICOLON")
        temp_result = self._new_temp()
        self.intermediate_code.append(f"{temp_result} = {right.value} {operator.value} {value.value}")
        return ("assign", left.value, temp_result)

    def _consume(self, expected_type):
        if self.current_token and self.current_token.type == expected_type:
            token = self.current_token
            print(f"Consuming token: {token.type}")
            self.current_token = self.tokens.next_token()
            return token
        else:
            raise SyntaxError(f"Expected token {expected_type} but got {self.current_token.type}")

    def _new_temp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    def _new_label(self):
        label = f"L{self.temp_count}"
        self.temp_count += 1
        return label

# Sample usage with tokenizer and parser
code = "if (x > 5) { x = x - 1; }"
tokenizer = Tokenizer(code)
tokens = tokenizer
parser = Parser(tokens)
