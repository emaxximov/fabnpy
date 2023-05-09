from fabnpy.ientities import Entity
from fabnpy.ipatterns import Pattern
import pytest


@pytest.fixture
def base_entity():
  return Entity('pressure', ['p<100kPa', 'p>100kPa'])


@pytest.fixture
def pattern():
  e1 = Entity('temperature', ['t<0C', 't>0C'])
  e2 = Entity('pressure', ['p<100kPa', 'p>100kPa'])
  kp = Pattern([e1, e2], [(0.1, 0.1), (0.2, 0.2), (0.4, 0.4), (0.3, 0.3)])
  return kp


@pytest.fixture
def trivial_pattern():
  e = Entity('pressure', ['p<100kPa', 'p>100kPa'])
  kp = Pattern([e], [(0.3, 0.5), (0.4, 0.6)])
  return kp


@pytest.fixture
def broken_pattern():
  e = Entity('pressure', ['p<100kPa', 'p>100kPa'])
  kp = Pattern([e], [(0.1, 0.1), (0.1, 0.1)], {('p<100kPa',): (0.5, 0.5)})
  return kp
