import pytest


def test_entity_setters(base_entity):
  with pytest.raises(TypeError):
    base_entity.elements = []


def test_pattern_setters(trivial_pattern):
  with pytest.raises(TypeError):
    trivial_pattern.entities = []
  with pytest.raises(TypeError):
    trivial_pattern.probabilities = []
  with pytest.raises(TypeError):
    trivial_pattern.clarification = []


def test_conj_process(pattern):
  source = ('p<100kPa', )
  target = ('', 'p<100kPa')
  assert pattern._Pattern__conjunct_process(source) == target
  with pytest.raises(ValueError):
    pattern._Pattern__conjunct_process(('p<100kPa', 'p>100kPa'))


def test_pattern_update(pattern):
  target = [(0.1, 0.1), (0.2, 0.2), (1.0, 1.0), (0.3, 0.3)]
  pattern.update_probabilities(('p<100kPa', 't>0C'), (1.0, 1.0))
  assert pattern.probabilities == target

  target = {('t>0C', ''): (1.0, 1.0)}
  pattern.update_clarification(('t>0C',), (1.0, 1.0))
  assert pattern.clarification == target
