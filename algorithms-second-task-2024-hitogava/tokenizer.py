import enum


class DefTokenTypes(enum.Enum):
    EOF = 0
    NONE = 1
    WHITESPACE = 2
    COMMA = 3
    LEFT_BRACKET = 4
    RIGHT_BRACKET = 5

    NUMBER = 6
    IDENTIFIER = 7


class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __str__(self):
        return f"{self.type}, {self.value}"


class Tokenizer:
    def __init__(
        self, keywords, halved_keywords, token_types, input_buffer: str
    ) -> None:
        self.keywords = keywords
        self.halved = halved_keywords
        self.token_types = token_types

        self.cursor = 0
        self.start = 0
        self.back = 0
        self.input = input_buffer
        self.tokens = []

    def make_token(self, token_type, value):
        return Token(token_type, value)

    def is_end(self):
        return self.cursor >= len(self.input)

    def get_keyword(self, key):
        return None if key not in self.keywords else self.keywords[key]

    def get_halved_keyword(self, key):
        return None if key not in self.halved else self.halved[key]

    def peek(self):
        return None if self.is_end() else self.input[self.cursor]

    def peek_next(self):
        return (
            None if self.cursor + 1 >= len(self.input) else self.input[self.cursor + 1]
        )

    def peek_prev(self):
        return None if self.cursor == 0 else self.input[self.cursor - 1]

    def match(self, expected):
        if self.is_end() or self.peek() != expected:
            return False
        self.move_cursor()

    def move_cursor(self):
        self.cursor += 1

    def advance_cursor(self):
        char = self.peek()
        self.move_cursor()
        return char

    def read_identifier(self):
        while not self.is_end() and (
            str.isalpha(self.peek()) or str.isdigit(self.peek()) or self.peek() in '-_'
        ):
            # self.advance_cursor()
            self.move_cursor()

    def read_number(self):
        while not self.is_end() and str.isdigit(self.peek()):
            self.move_cursor()
        if self.peek() == ".":
            self.move_cursor()
            while not self.is_end() and str.isdigit(self.peek()):
                self.move_cursor()

    def skip_whitespaces(self):
        while True:
            char = self.peek()
            if char == " ":
                self.move_cursor()
            else:
                return

    def match_next_token(self, expected: Token):
        self.back = self.cursor
        token = self.get_token()
        if token.type == expected:
            return True
        self.cursor = self.back
        return False

    def get_token(self) -> Token:
        self.skip_whitespaces()
        self.start = self.cursor
        if self.is_end():
            return self.make_token(DefTokenTypes.EOF, "Eof")
        char = self.advance_cursor()
        if char == ",":
            return self.make_token(DefTokenTypes.COMMA, ",")
        elif char == "[":
            return self.make_token(DefTokenTypes.LEFT_BRACKET, "[")
        elif char == "]":
            return self.make_token(DefTokenTypes.RIGHT_BRACKET, "]")
        else:
            if str.isalpha(char):
                self.read_identifier()
                substring = self.input[self.start : self.cursor]
                keyword_type = self.get_keyword(substring.lower())
                if not keyword_type:
                    return self.make_token(DefTokenTypes.IDENTIFIER, substring)
                return self.make_token(self.keywords[substring.lower()], substring.lower())
            elif str.isdigit(char):
                self.read_number()
                substring = self.input[self.start : self.cursor]
                return self.make_token(DefTokenTypes.NUMBER, substring)
            return self.make_token(DefTokenTypes.NONE, "")

    def tokenize(self):
        tokens = []
        while True:
            tkn = self.get_token()
            tokens.append(tkn)
            if tkn.type == DefTokenTypes.EOF:
                break
        return tokens
