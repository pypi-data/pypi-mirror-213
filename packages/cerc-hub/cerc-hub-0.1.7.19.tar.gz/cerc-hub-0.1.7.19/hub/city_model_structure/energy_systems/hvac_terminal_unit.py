"""
HvacTerminalUnit module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
from typing import Union


class HvacTerminalUnit:
  """
  HvacTerminalUnit class
  """
  def __init__(self):
    self._type = None

  @property
  def type(self) -> Union[None, str]:
    """
    Get type of hvac terminal unit defined for a thermal zone
    :return: None or str
    """
    return self._type

  @type.setter
  def type(self, value):
    """
    Set type of hvac terminal unit defined for a thermal zone
    :param value: str
    """
    if value is not None:
      self._type = str(value)
