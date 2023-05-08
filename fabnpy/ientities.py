class Entity:
  def __init__(self, name: str, elements: list[str]):
    self.name = name
    self.__elements = elements
    self.validate()

  @property
  def elements(self):
    return self.__elements

  @elements.setter
  def elements(self, value):
    raise TypeError('Entity object does not support elements assignment')

  def validate(self):
    assert len(set(self.__elements)) == len(self.__elements)
    for e in self.__elements:
      assert all(not smb.isspace() for smb in e)

  def find(self, var: str):
    """number of variable in entity, -1 if variable is not included"""
    try:
      return self.__elements.index(var)
    except ValueError:
      return -1

  def __len__(self):
    return len(self.__elements)
