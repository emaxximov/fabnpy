basis = [
  ('t<0C', 'p<100kPa'),
  ('t<0C', 'p>100kPa'),
  ('t>0C', 'p<100kPa'),
  ('t>0C', 'p>100kPa')
]


def test_view(pattern):
  target = basis
  arr = []
  for i in range(pattern.basis):
    arr.append(pattern.view(i))
  assert target == arr


def test_view_as_num(pattern):
  target = list(range(pattern.basis))
  arr = []
  for quant in basis:
    arr.append(pattern.view_as_number(quant))
  assert target == arr


def test_vector_as_num(pattern):
  target = 1
  vector = [0, 1]
  num = pattern.vector_as_number(vector)
  assert target == num


def test_get_mask(pattern):
  target = [-1, 0]
  conjunct = ('', 'p<100kPa',)
  vector = pattern._Pattern__get_mask(conjunct)
  assert target == vector


def test_as_vector(pattern):
  target = [1, 0, 1, 0]
  conjunct = ('p<100kPa',)
  vector = pattern.as_vector(conjunct)
  assert target == vector


def test_conjunct_process(pattern):
  target = ('', 'p<100kPa')
  conjunct = ('p<100kPa',)
  processed_conjunct = pattern._Pattern__conjunct_process(conjunct)
  assert target == processed_conjunct
