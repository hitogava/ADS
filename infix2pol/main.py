from utils import TokenType, Stack, tokenize


def infix_to_polish(expr: str):
    result = ""
    st = Stack()
    tokens = tokenize(expr)
    for t in tokens:
        if t.tok_type == TokenType.op:
            if st.empty():
                st.push(t.value)
            else:
                if t.value.precedence < st.peek().precedence or t.value.content == "(":
                    st.push(t.value)
                elif t.value.content == ")":
                    while st.peek().content != "(":
                        result += st.pop().content + " "
                    # extra '(' on top of the stack
                    st.pop()
                else:
                    while (
                        not st.empty()
                        and st.peek().content != "("
                        and (
                            t.value.precedence > st.peek().precedence
                            or st.peek().assoc == 1
                            and st.peek().precedence == t.value.precedence
                        )
                    ):
                        result += st.pop().content + " "
                    st.push(t.value)
        elif t.tok_type == TokenType.number:
            result += t.value + " "
    while not st.empty():
        result += st.pop().content + " "
    return result[: len(result) - 1]


def tests():
    expr = "12 + 38 + 4 - 5"
    assert infix_to_polish(expr) == "12 38 + 4 + 5 -"

    expr = "1 - 5 * 2"
    assert infix_to_polish(expr) == "1 5 2 * -"

    expr = "1 - 2 * 3 + 2"
    assert infix_to_polish(expr) == "1 2 3 * - 2 +"

    expr = "1 + 4 & 7"
    assert infix_to_polish(expr) == "1 4 + 7 &"

    expr = "1 && 4 & 7"
    assert infix_to_polish(expr) == "1 4 7 & &&"

    # parenthesis operations
    expr = "(1 + 3) * 6"
    assert infix_to_polish(expr) == "1 3 + 6 *"

    expr = "((1) + (3) * (8))"
    assert infix_to_polish(expr) == "1 3 8 * +"

    expr = "(((1) + (((3)))) * 9)"
    assert infix_to_polish(expr) == "1 3 + 9 *"

    expr = "1 + (2 * 3)"
    assert infix_to_polish(expr) == "1 2 3 * +"

    expr = "((1 + (2 * 3) + 8) / (2 / 3))"
    assert infix_to_polish(expr) == "1 2 3 * + 8 + 2 3 / /"
    
    # unary operations
    expr = "~1 + ~3"
    assert infix_to_polish(expr) == "1 ~ 3 ~ +"

    expr = "-3 + 6"
    assert infix_to_polish(expr) == "3 - 6 +"

    expr = "-(3 + 6)"
    assert infix_to_polish(expr) == "3 6 + -"

    expr = "-1 - -2"
    assert infix_to_polish(expr) == "1 - 2 - -"

    expr = "-1 * +2"
    assert infix_to_polish(expr) == "1 - 2 + *"

    print("ALL TESTS PASSED")


tests()
