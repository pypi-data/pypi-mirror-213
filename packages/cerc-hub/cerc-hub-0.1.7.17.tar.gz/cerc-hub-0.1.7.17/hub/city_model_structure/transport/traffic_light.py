"""
Traffic light module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
Code contributors: Guille guille.gutierrezmorote@concordia.ca
"""

import ast
from typing import List, Union
from hub.city_model_structure.transport.phase import Phase
from hub.city_model_structure.transport.traffic_node import TrafficNode


class TrafficLight(TrafficNode):
  """
  Traffic light class
  """
  def __init__(self, name, coordinates, offset, phases=None, edges=None, right_on_red=False):
    super().__init__(name, coordinates, edges=edges, node_type='TrafficLight')
    if phases is None:
      phases = []
    self._right_on_red = right_on_red
    self._offset = offset
    self._phases = phases

  @property
  def right_on_red(self) -> Union[None, bool]:
    """
    Get if is possible to turn right when the traffic light is red
    :return: None or Boolean
    """
    return self._right_on_red

  @right_on_red.setter
  def right_on_red(self, value):
    """
    Get if is possible to turn right when the traffic light is red
    :param value: Boolean
    """
    if value is not None:
      self._right_on_red = ast.literal_eval(value)

  @property
  def offset(self) -> Union[None, int]:
    """
    Get program initial time offset
    :return: None or int
    """
    return self._offset

  @offset.setter
  def offset(self, value):
    """
    Set program initial time offset
    :param value: int
    """
    if value is not None:
      self._offset = int(value)

  @property
  def phases(self) -> List[Phase]:
    """
    Get traffic light logic phases
    :return: [Phase]
    """
    return self._phases

  @phases.setter
  def phases(self, value):
    """
    Set traffic light logic phases
    :param value: [Phase]
    """
    self._phases = value
