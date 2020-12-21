from pypargen import grammar


def test_palindrome():
    palindrome = grammar.Grammar([('S', ['"a"', 'S', '"a"']),
                                  ('S', ['"b"', 'S', '"b"']), ('S', [])])
    assert palindrome.start == 'S'
    assert palindrome.terminals == {'"a"', '"b"'}
    assert palindrome.nonterminals == {'S'}
    assert palindrome.first(['S']) == {'"a"', '"b"', 'ϵ'}
    assert str(palindrome) == """S -> "a" S "a"
S -> "b" S "b"
S -> ϵ"""


def test_math():
    math_rules = [("atom", ['"[1-9][0-9]*"']),
                  ("atom", [r'"\("', "sub", r'"\)"']),
                  ("div", ["div", '"/"', "atom"]), ("div", ["atom"]),
                  ("mul", ["mul", r'"\*"', "div"]), ("mul", ["div"]),
                  ("add", ["add", r'"\+"', "mul"]), ("add", ["mul"]),
                  ("sub", ["sub", '"-"', "add"]), ("sub", ["add"])]
    math = grammar.Grammar(math_rules, 'sub')
    assert math.start == 'sub'
    assert math.terminals == {
        '"[1-9][0-9]*"', r'"\("', r'"\)"', '"/"', r'"\*"', r'"\+"', '"-"'
    }
    assert math.nonterminals == {"atom", "div", "mul", "add", "sub"}
    assert math.first(["sub"]) == {'"[1-9][0-9]*"', r'"\("'}
    assert math.first(["add"]) == {'"[1-9][0-9]*"', r'"\("'}
    assert math.first(["mul"]) == {'"[1-9][0-9]*"', r'"\("'}
    assert math.first(["div"]) == {'"[1-9][0-9]*"', r'"\("'}
    assert math.first(["atom"]) == {'"[1-9][0-9]*"', r'"\("'}
