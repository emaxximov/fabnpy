def test_local_cons_false(broken_pattern):
  p = broken_pattern.local_cons()
  assert not p


def test_local_cons_true(trivial_pattern):
  p = trivial_pattern.local_cons()
  assert p
  assert trivial_pattern.probabilities[0] == (0.4, 0.5)
  assert trivial_pattern.probabilities[1] == (0.5, 0.6)
