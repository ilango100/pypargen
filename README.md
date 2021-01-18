# Pypargen

Pypargen is a Parser generator in python. It creates parsers for LR(1) grammars. Currently pypargen cannot create parser for LR(k > 1). You can write grammar in a simple format (which I call `grm` format).


## Example: Math expressions

The grammar for math expressions is:

```
atom -> "[1-9][0-9]*"
atom -> "(" sub ")"
div  -> div "/" atom
div  -> atom
mul  -> mul "*" div
mul  -> div
add  -> add "+" mul
add  -> mul
sub  -> sub "-" add
sub  -> add
expr -> sub "\n\n*"
```

For every rule, you need to provide a callback that will take the same number of arguments as right side of every rule and returns the object that represents the left side of the rule.

For example for `add -> add "+" mul` rule, the callback could be:
```python
def add(a, _plus, b):
	return a + b
```

```python
import pypargen as pgen

# Parse the grm file first
gparser = pgen.GrmParser()
with open("math.grm") as fp:
	math_grammar = parser.parse(fp)

# See examples/math.py for example of callbacks.
parser = pgen.Parser(math_grammar, callbacks)
result = parser.parse(sys.stdin)
print(result)
```
