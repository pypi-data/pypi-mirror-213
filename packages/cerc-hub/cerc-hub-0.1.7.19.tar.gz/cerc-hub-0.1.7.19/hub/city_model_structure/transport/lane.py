"""
Lane module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from typing import List, Union


class Lane:
  """
  Lane class
  """

  def __init__(self):
    self._index = None
    self._allow = None
    self._disallow = None
    self._change_left = None
    self._change_right = None
    self._speed = None
    self._width = None

  @property
  def index(self) -> Union[None, int]:
    """
    Get lane index
    The enumeration index of the lane (0 is the rightmost lane, <NUMBER_LANES>-1 is the leftmost one)
    :return: None or int
    """
    return self._index

  @index.setter
  def index(self, value):
    """
    Set lane index
    The enumeration index of the lane (0 is the rightmost lane, <NUMBER_LANES>-1 is the leftmost one)
    :param value: int
    """
    if value is not None:
      self._index = int(value)

  @property
  def allow(self) -> Union[None, List[str]]:
    """
    Get the list of allowed vehicle classes
    :return: None or [str]
    """
    return self._allow

  @allow.setter
  def allow(self, value):
    """
    Set the list of allowed vehicle classes setter
    :param value: [str]
    """
    if value is not None:
      self._allow = [str(i) for i in value]

  @property
  def disallow(self) -> Union[None, List[str]]:
    """
    Get the list of not allowed vehicle classes
    :return: None or [str]
    """
    return self._disallow

  @disallow.setter
  def disallow(self, value):
    """
    Get the list of not allowed vehicle classes setter
    :param value: [str]
    """
    if value is not None:
      self._disallow = [str(i) for i in value]

  @property
  def change_left(self) -> Union[None, List[str]]:
    """
    Get the list of vehicle classes that may change left from this lane
    :return: None or [str]
    """
    return self._change_left

  @change_left.setter
  def change_left(self, value):
    """
    Set the list of vehicle classes that may change left from this lane
    :param value: [str]
    """
    if value is not None:
      self._change_left = [str(i) for i in value]

  @property
  def change_right(self) -> Union[None, List[str]]:
    """
    Get the list of vehicle classes that may change right from this lane
    :return: None or [str]
    """
    return self._change_right

  @change_right.setter
  def change_right(self, value):
    """
    Set the list of vehicle classes that may change right from this lane
    :param value: [str]
    """
    if value is not None:
      self._change_right = [str(i) for i in value]

  @property
  def speed(self) -> Union[None, float]:
    """
    Get the lane speed in m/s
    :return: None or float
    """
    return self._speed

  @speed.setter
  def speed(self, value):
    """
    Set the lane speed in m/s
    :param value: float
    """
    if value is not None:
      self._speed = float(value)

  @property
  def width(self) -> Union[None, float]:
    """
    Get the lane width in meters
    :return: None or float
    """
    return self._width

  @width.setter
  def width(self, value):
    """
    Set the lane width in meters
    :param value: float
    """
    if value is not None:
      self._width = float(value)
