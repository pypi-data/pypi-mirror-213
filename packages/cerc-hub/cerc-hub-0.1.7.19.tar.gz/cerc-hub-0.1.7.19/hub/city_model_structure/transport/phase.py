"""
Phase module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from typing import List, Union


class Phase:
  """
  Phase class
  """

  def __init__(self):
    self._duration = None
    self._state = None
    self._min_duration = None
    self._max_duration = None
    self._name = None
    self._next = None

  @property
  def duration(self) -> Union[None, int]:
    """
    Get phase duration in seconds
    :return: None or int
    """
    return self._duration

  @duration.setter
  def duration(self, value):
    """
    Set phase duration in seconds
    :param value: int
    """
    if value is not None:
      self._duration = int(value)

  @property
  def state(self) -> Union[None, List[str]]:
    """
    Get the list of signal states
    :return: None or [str]
    """
    return self._state

  @state.setter
  def state(self, value):
    """
    Set the list of signal states
    :param value: [str]
    """
    if value is not None:
      self._state = [str(i) for i in value]

  @property
  def min_duration(self) -> Union[None, int]:
    """
    Get phase minimum duration in seconds
    :return: None or int
    """
    if self._min_duration is None:
      self._min_duration = self._duration
    return self._min_duration

  @min_duration.setter
  def min_duration(self, value):
    """
    Set phase minimum duration in seconds
    :param value: int
    """
    if value is not None:
      self._min_duration = int(value)

  @property
  def max_duration(self) -> Union[None, int]:
    """
    Get phase maximum duration in seconds
    :return: None or int
    """
    if self._max_duration is None:
      self._max_duration = self._duration
    return self._max_duration

  @max_duration.setter
  def max_duration(self, value):
    """
    Set phase maximum duration in seconds
    :param value: int
    """
    if value is not None:
      self._max_duration = int(value)

  @property
  def name(self) -> Union[None, str]:
    """
    Get phase name
    :return: None or str
    """
    return self._name

  @name.setter
  def name(self, value):
    """
    Set phase name
    :param value: str
    """
    if value is not None:
      self._name = str(value)

  @property
  def next(self) -> Union[None, List[int]]:
    """
    Get the next phase in the cycle after the current.
    This is useful when adding extra transition phases to a traffic light plan which are not part of every cycle.
    Traffic lights of type 'actuated' can make use of a list of indices for selecting among alternative
    successor phases.
    :return: None or [int]
    """
    return self._next

  @next.setter
  def next(self, value):
    """
    Get the next phase in the cycle after the current.
    This is useful when adding extra transition phases to a traffic light plan which are not part of every cycle.
    Traffic lights of type 'actuated' can make use of a list of indices for selecting among alternative
    successor phases.
    :param value: [int]
    """
    if value is not None:
      self._next = [int(i) for i in value]
