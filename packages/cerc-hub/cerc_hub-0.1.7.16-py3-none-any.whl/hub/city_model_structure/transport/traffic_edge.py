"""
Traffic edge module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
Code contributors: Guille guille.gutierrezmorote@concordia.ca
"""

from typing import List, Union
from hub.city_model_structure.attributes.edge import Edge
from hub.city_model_structure.transport.traffic_node import TrafficNode
from hub.city_model_structure.transport.lane import Lane


class TrafficEdge(Edge):
  """
  TrafficEdge class
  Each edge is unidirectional and starts at the "from" node and ends at the "to" node
  """

  def __init__(self, name, nodes, priority, speed, lanes, length, allows=None, disallows=None, sidewalk_width=None,
               edge_type='TrafficEdge'):
    super().__init__(name, nodes)
    self._edge_type = edge_type
    self._lanes = lanes
    self._priority = priority
    self._speed = speed
    self._length = length
    self._allows = allows
    self._disallows = disallows
    self._sidewalk_width = sidewalk_width

  @property
  def edge_type(self):
    """
    Get the edge type
    :return: str
    """
    return self._edge_type

  @property
  def nodes(self) -> List[TrafficNode]:
    """
    Get delimiting nodes for the edge
    :return: [TrafficNode]
    """
    return self._nodes

  @property
  def lanes(self) -> List[Lane]:
    """
    Get the lanes on an edge
    :return: List[Lane]
    """
    return self._lanes

  @lanes.setter
  def lanes(self, value):
    """
    Set the lanes on an edge
    :param value: List[Lane]
    """
    self._lanes = value

  @property
  def priority(self) -> Union[None, int]:
    """
    Get the priority between different road types.
    It starts with one; higher numbers represent more important roads.
    :return: None or int
    """
    return self._priority

  @priority.setter
  def priority(self, value):
    """
    Set the priority between different road types.
    It starts with one; higher numbers represent more important roads.
    :param value: int
    """
    if value is not None:
      self._priority = int(value)

  @property
  def speed(self) -> Union[None, float]:
    """
    Get he speed limit in m/s
    :return: None or float
    """
    return self._speed

  @speed.setter
  def speed(self, value):
    """
    Set the speed limit in m/s
    :param value: float
    """
    if value is not None:
      self._speed = float(value)

  @property
  def length(self) -> Union[None, float]:
    """
    Get the lane length in meters
    :return: None or float
    """
    return self._length

  @length.setter
  def length(self, value):
    """
    Set the lane length in meters
    :param value: float
    """
    if value is not None:
      self._length = float(value)

  @property
  def allows(self) -> Union[None, List[str]]:
    """
    Get the list of allowed vehicle classes
    :return: None or [str]
    """
    return self._allows

  @allows.setter
  def allows(self, value):
    """
    Set the list of allowed vehicle classes
    :param value: [str]
    """
    if value is not None:
      self._allows = [str(i) for i in value]

  @property
  def disallows(self) -> Union[None, List[str]]:
    """
    Get the list of not allowed vehicle classes
    :return: None or [str]
    """
    return self._disallows

  @disallows.setter
  def disallows(self, value):
    """
    Set the list of not allowed vehicle classes
    :param value: [str]
    """
    if value is not None:
      self._disallows = [str(i) for i in value]
