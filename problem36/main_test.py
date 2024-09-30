from main import solution

def check(test_number: int):
    with open(f"./tests/{test_number}.in", "r") as inp:
        with open(f"./tests/{test_number}.exp", "r") as out:
            data = inp.read()
            out = out.read().strip('\n')

            assert out == solution(data)

def test1():
    check(1)

def test2():
    check(2)

def test3():
    check(3)

def test4():
    check(4)

def test5():
    check(5)
