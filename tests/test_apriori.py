import pytest


def test_apriori_imp(pattern):
  formula = 't<0C > p<100kPa'
  p = pattern.apriori(formula)
  assert p == (0.8, 0.8)


def test_apriori_xor(pattern):
  formula = 't<0C + p<100kPa'
  p = pattern.apriori(formula)
  assert p == (0.6, 0.6)


def test_apriori_eq(pattern):
  formula = 't<0C = p<100kPa'
  p = pattern.apriori(formula)
  assert p == (0.4, 0.4)


def test_apriori_or(pattern):
  formula = 't<0C | p<100kPa'
  p = pattern.apriori(formula)
  assert p == (0.7, 0.7)


def test_apriori_error(broken_pattern):
  formula = 'p<100kPa'
  with pytest.raises(ValueError):
    broken_pattern.apriori(formula)
