import pytest
from fabnpy.iutils import dijkstra, calc


def test_dijkstra():
  formula = '1 | 2'
  with pytest.raises(ValueError):
    for _ in dijkstra(formula):
      pass
  target = ['1', '0', '|', '0', '|']
  formula = '1|0|0'
  res = []
  for i in dijkstra(formula):
    res.append(i)
  assert res == target
  target = ['1', '0', '|', '1', '~', '&']
  formula = '(1|0)&~1'
  res = []
  for i in dijkstra(formula):
    res.append(i)
  assert res == target
  target = ['1', '0', '1', '~', '&', '|']
  formula = '1|0&~1'
  res = []
  for i in dijkstra(formula):
    res.append(i)
  assert res == target


def test_calc():
  target = 0
  formula = '(1|0)&~1'
  assert calc(formula) == target
  target = 1
  formula = '1|0&~1'
  assert calc(formula) == target
#
#
# def test_apriori_eq(pattern):
#   formula = 't<0C = p<100kPa'
#   p = pattern.apriori(formula)
#   assert p == (0.4, 0.4)
#
#
# def test_apriori_or(pattern):
#   formula = 't<0C | p<100kPa'
#   p = pattern.apriori(formula)
#   assert p == (0.7, 0.7)
#
#
# def test_apriori_error(broken_pattern):
#   formula = 'p<100kPa'
#   with pytest.raises(ValueError):
#     broken_pattern.apriori(formula)
