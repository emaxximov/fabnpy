from fabnpy.ioperators import OPERATORS, NOT


def dijkstra(formula):
  stack = []
  for token in formula:
    # we expect all operators to be right-associative
    if token in OPERATORS:
      while stack and stack[-1] != "(" and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
        yield stack.pop()
      stack.append(token)
    elif token == ")":
      while stack:
        x = stack.pop()
        if x == "(":
          break
        yield x
    elif token == "(":
      stack.append(token)
    elif token == '1' or token == '0':
      yield token
    else:
      raise ValueError('Bad token in formula')
  while stack:
    yield stack.pop()


def calc(formula) -> bool:
  polish = dijkstra(formula)
  stack = []
  for token in polish:
    if token in OPERATORS:
      if token != NOT:
        y, x = stack.pop(), stack.pop()
        stack.append(OPERATORS[token][1](x, y))
      else:
        x = stack.pop()
        stack.append(OPERATORS[token][1](x))
    else:
      stack.append(token)
  print(stack[0])
  return stack[0]
