from typing import Optional
from fabnpy.ientities import Entity
from fabnpy.iutils import calc
from functools import cached_property, lru_cache
from scipy.optimize import linprog
from tqdm import tqdm
from itertools import product


Pair = tuple[float, float]
Conjunct = tuple[str, ...]
Map = dict[Conjunct, Pair]

SUPPRESS_OUTPUT = True


# noinspection PyDeprecation
class Pattern:
  def __init__(self,
               entities: list[Entity],
               probabilities: Optional[list[Pair]] = None,
               clarification: Optional[Map] = None):
    self.__entities = entities
    self.__n = len(entities)
    if probabilities is None:
      probabilities = [(0.0, 1.0)] * self.basis
    self.__probabilities = probabilities
    if clarification is None:
      clarification: Map = {}
    self.__clarification: Map = {}
    for c in clarification.items():
      self.update_clarification(c[0], c[1])
    self.validate()

  @property
  def entities(self):
    return self.__entities

  @entities.setter
  def entities(self, value):
    raise TypeError('Pattern object does not support entities assignment')

  @property
  def probabilities(self):
    return self.__probabilities

  @probabilities.setter
  def probabilities(self, value):
    raise TypeError('Pattern object does not support probabilities assignment')

  @property
  def clarification(self):
    return self.__clarification

  @clarification.setter
  def clarification(self, value):
    raise TypeError('Pattern object does not support clarification assignment')

  def validate(self):
    assert len(self.__probabilities) == self.basis
    for p in self.__probabilities:
      assert 0 <= p[0] <= p[1] <= 1
    total_vars = 0
    vars_set = set()
    for e in self.__entities:
      total_vars += len(e)
      vars_set.update(e.elements)
    assert total_vars == len(vars_set)
    for c in self.__clarification:
      p = self.__clarification[c]
      assert 0 <= p[0] <= p[1] <= 1
      for v in c:
        assert self.find(v) is not None

  @property
  def has_clarification(self) -> bool:
    return len(self.__clarification) != 0

  def update_probabilities(self, conjunct: Conjunct, prob: Pair):
    """set one probability"""
    assert 0 <= prob[0] <= prob[1] <= 1
    processed_conjunct = self.__conjunct_process(conjunct)
    self.__probabilities[self.view_as_number(processed_conjunct)] = prob

  def update_clarification(self, conjunct: Conjunct, prob: Pair):
    """set one clarification"""
    assert 0 <= prob[0] <= prob[1] <= 1
    processed_conjunct = self.__conjunct_process(conjunct)
    self.__clarification[processed_conjunct] = prob

  @lru_cache
  def find(self, var: str) -> Optional[tuple[int, int]]:
    """number of entity that includes the variable and number of variable in that entity"""
    for e_ind, e in enumerate(self.__entities):
      for el_ind, el in enumerate(e.elements):
        if var == el:
          return e_ind, el_ind

  @cached_property
  def sizes(self) -> list[int]:
    """list of entity sizes"""
    return [len(e) for e in self.__entities]

  @cached_property
  def prod(self) -> list[int]:
    """product on the suffix of sizes"""
    total = 1
    res = [1]
    for i in self.sizes[::-1]:
      total *= i
      res.append(total)
    return res

  @cached_property
  def basis(self) -> int:
    """number of nonzero quants"""
    return self.prod[-1]

  def view(self, num: int) -> Conjunct:
    """basic conjunct by number"""
    res = []
    for i in range(self.__n):
      ind = num // self.prod[self.__n - 1 - i]
      res.append(self.__entities[i].elements[ind])
      num %= self.prod[self.__n - 1 - i]
    return tuple(res)

  def view_as_number(self, view: Conjunct) -> int:
    """number by basic conjunct view"""
    res = 0
    processed_view = self.__conjunct_process(view)
    for i, v in enumerate(processed_view):
      res += self.__entities[i].find(v) * self.prod[self.__n - 1 - i]
    return res

  def vector_as_number(self, vector: list[int]) -> int:
    """number by basic conjunct vector"""
    res = 0
    for i, v in enumerate(vector):
      res += v * self.prod[self.__n - 1 - i]
    return res

  def __conjunct_process(self, conjunct: Conjunct) -> Conjunct:
    res = []
    conjunct_set = set(conjunct)
    for e in self.__entities:
      res.append('')
      for var in conjunct_set:
        ind = e.find(var)
        if ind > -1:
          res[-1] = var
          conjunct_set.discard(var)
          break
    if len(conjunct_set) > 0:
      raise ValueError('Redundant conjunct')
    return tuple(res)

  def __get_mask(self, processed_view: Conjunct) -> list[int]:
    res = []
    for ind, var in enumerate(processed_view):
      res.append(self.__entities[ind].find(var))
    return res

  def as_vector(self, conjunct: Conjunct, already_processed: bool = False):
    """arbitrary conjunct as sum of basic conjuncts"""
    res = [0] * self.basis
    processed_conjunct = conjunct if already_processed else self.__conjunct_process(conjunct)
    mask = self.__get_mask(processed_conjunct)
    source = []
    for ind, restriction in enumerate(mask):
      if restriction == -1:
        source.append(range(self.sizes[ind]))
      else:
        source.append([restriction])
    for vector in product(*source):
      res[self.vector_as_number(vector)] = 1
    return res

  @lru_cache
  def __get_r(self):
    R, r = [], []
    for conj, sum_est in self.__clarification.items():
      vector = self.as_vector(conj, already_processed=True)
      R.append(vector)
      r.append(sum_est[1])
      for i in range(self.basis):
        vector[i] *= -1
      R.append(vector)
      r.append(-sum_est[0])
    return R, r

  def local_cons(self, precision: int = 2) -> bool:
    """inplace maintaining local consistency. true if pattern is consistent"""
    new_lower_bounds, new_upper_bounds = [], []

    R, r = self.__get_r()

    target = [0] * self.basis

    for i in tqdm(range(self.basis), disable=SUPPRESS_OUTPUT):
      target[i] = 1
      try_new_lower_bound = linprog(target,
                                    A_eq=[[1] * self.basis],
                                    b_eq=[1],
                                    A_ub=R if len(R) > 0 else None,
                                    b_ub=r if len(r) > 0 else None,
                                    bounds=self.__probabilities)
      if try_new_lower_bound.success:
        new_lower_bounds.append(round(try_new_lower_bound.fun, precision))
      else:
        return False

      target[i] = -1
      try_new_upper_bound = linprog(target,
                                    A_eq=[[1] * self.basis],
                                    b_eq=[1],
                                    A_ub=R if len(R) > 0 else None,
                                    b_ub=r if len(r) > 0 else None,
                                    bounds=self.__probabilities)
      if try_new_upper_bound.success:
        new_upper_bounds.append(round(-try_new_upper_bound.fun, precision))
      else:
        return False
      target[i] = 0

    self.__probabilities = [(i, j) for i, j in zip(new_lower_bounds, new_upper_bounds)]
    return True

  def apriori(self, formula: str, precision: int = 2) -> Pair:
    """apriori inference"""
    target = [0] * self.basis
    source = [range(self.sizes[ind]) for ind in range(self.__n)]
    basis_index = 0
    for implementation in product(*source):
      subst_formula = formula
      for e_ind, e in enumerate(self.__entities):
        for el_ind, el in enumerate(e.elements):
          if implementation[e_ind] == el_ind:
            subst_formula = subst_formula.replace(el, '1')
          else:
            subst_formula = subst_formula.replace(el, '0')
      subst_formula = subst_formula.replace(' ', '')
      value = calc(subst_formula)
      target[basis_index] = value
      basis_index += 1

    R, r = self.__get_r()

    try_lower_bound = linprog(target,
                              A_eq=[[1] * self.basis],
                              b_eq=[1],
                              A_ub=R if len(R) > 0 else None,
                              b_ub=r if len(r) > 0 else None,
                              bounds=self.__probabilities)
    if not try_lower_bound.success:
      raise ValueError('Pattern is not consistent')

    for i in range(self.basis):
      target[i] *= -1
    try_upper_bound = linprog(target,
                              A_eq=[[1] * self.basis],
                              b_eq=[1],
                              A_ub=R if len(R) > 0 else None,
                              b_ub=r if len(r) > 0 else None,
                              bounds=self.__probabilities)
    if not try_upper_bound.success:
      raise ValueError('Pattern is not consistent')

    return round(try_lower_bound.fun, precision), round(-try_upper_bound.fun, precision)
