from enum import Enum

class Stack:
    def __init__(
        self,
    ) -> None:
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def empty(self):
        return len(self.stack) == 0

    def pop(self):
        if self.empty():
            return None
        last = self.stack[-1]
        self.stack = self.stack[: len(self.stack) - 1]
        return last

    def peek(self):
        return None if self.empty() else self.stack[-1]


# assoc: 0 - Right-to-left
# assoc: 1 - Left-to-right
class Operator:
    def __init__(self, value: str, precedence: int, assoc: int) -> None:
        self.content = value
        self.precedence = precedence
        self.assoc = assoc

    def __str__(self) -> str:
        return f"{self.content}, {self.precedence}, {self.assoc}"


class TokenType(Enum):
    op = (0,)
    number = 1


class Token:
    def __init__(self, tt: TokenType, value) -> None:
        self.tok_type = tt
        self.value = value

    def __str__(self) -> str:
        return f"type: {self.tok_type.name}, value: {self.value}"


def tokenize(expr: str) -> list[Token]:
    tokens = []
    j = -1
    skip = False
    prev_tkn_num = False
    for i, ch in enumerate(expr):
        if skip == 1:
            skip = 0
            continue
        if ch.isspace():
            continue
        if ch.isdigit():
            if j == -1:
                j = i
            if i == len(expr) - 1 or not (expr[i + 1].isdigit()):
                val = expr[j : i + 1]
                prev_tkn_num = True
                tokens.append(Token(TokenType.number, val))
                j = -1
            else:
                continue
        else:
            op = None
            if ch == "~":
                op = Operator(ch, 2, 0)
            elif ch == "!":
                op = Operator(ch, 2, 0)
                # !=
            elif ch == "(":
                op = Operator(ch, 100, 1)
            elif ch == ")":
                op = Operator(ch, 100, 1)
            elif ch in "*/%":
                op = Operator(ch, 3, 1)
            elif ch in "+-":
                if prev_tkn_num == True:
                    op = Operator(ch, 4, 1)
                else:
                    op = Operator(ch, 2, 0)
            elif ch == "<":
                if i != len(expr) - 1 and expr[i + 1] == "<":
                    op = Operator("<<", 5, 1)
                elif i != len(expr) - 1 and expr[i + 1] == "<=":
                    op = Operator("<=", 6, 1)
                else:
                    op = Operator("<", 6, 1)
            elif ch == "&":
                if i != len(expr) - 1 and expr[i + 1] == "&":
                    op = Operator("&&", 11, 1)
                    skip = 1
                else:
                    op = Operator(ch, 8, 1)
            elif ch == "^":
                op = Operator(ch, 9, 1)
            elif ch == "|":
                if i != len(expr) - 1 and expr[i + 1] == "|":
                    op = Operator("||", 12, 1)
                    skip = 1
                else:
                    op = Operator(ch, 10, 1)
            else:
                print("Unknown token")
                return []
            prev_tkn_num = True if ch in "()" else False
            tokens.append(Token(TokenType.op, op))
    return tokens
