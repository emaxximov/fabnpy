OPERATORS = \
    {'&': (5, lambda x, y: min(int(x), int(y))), '|': (4, lambda x, y: max(int(x), int(y))),
     '+': (3, lambda x, y: abs(int(x) - int(y))), '>': (2, lambda x, y: int(int(x) == 0 or int(y) == 1)),
     '=': (1, lambda x, y: int(int(x) == int(y))), '~': (6, lambda x: int(not int(x)))}

NOT = '~'
