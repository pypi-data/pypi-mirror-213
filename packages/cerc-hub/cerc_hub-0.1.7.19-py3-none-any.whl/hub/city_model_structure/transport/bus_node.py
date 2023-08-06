"""
Bus node module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from typing import List, TypeVar

from hub.city_model_structure.attributes.node import Node
from hub.city_model_structure.attributes.point import Point

BusEdge = TypeVar('BusEdge')


class BusNode(Node):
  """
  BusNode class
  """

  def __init__(self, name, coordinates, node_type='BusNode', edges=None):
    super().__init__(name, edges)
    self._coordinates = coordinates
    self._node_type = node_type

  @property
  def node_type(self):
    """
    Get node type
    :return: str
    """
    return self._node_type

  @property
  def coordinates(self) -> Point:
    """
    Get node coordinates
    :return: Point
    """
    return self._coordinates

  @coordinates.setter
  def coordinates(self, value):
    """
    Set node coordinates
    :param value: Point
    """
    self._coordinates = value

  @property
  def edges(self) -> List[BusEdge]:
    """
    get edges delimited by the node
    :return: [BusEdge]
    """
    return self._edges
