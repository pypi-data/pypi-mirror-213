"""
TrafficNode module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
Code contributors: Guille guille.gutierrezmorote@concordia.ca
"""

from typing import List, TypeVar

from hub.city_model_structure.attributes.edge import Edge
from hub.city_model_structure.attributes.node import Node
from hub.city_model_structure.attributes.point import Point

Connection = TypeVar('Connection')
TrafficEdge = TypeVar('TrafficEdge')


class TrafficNode(Node):
  """
  TrafficNode class
  """

  def __init__(self, name, coordinates, node_type='TrafficNode', edges=None, prohibitions=None, connections=None):
    super().__init__(name, edges)
    if connections is None:
      connections = []
    if prohibitions is None:
      prohibitions = []
    self._coordinates = coordinates
    self._prohibitions = prohibitions
    self._connections = connections
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
  def edges(self) -> List[TrafficEdge]:
    """
    get edges delimited by the node
    :return: [TrafficEdge]
    """
    return self._edges

  @property
  def prohibitions(self) -> [(Edge, Edge)]:
    """
    Get node prohibitions
    :return: [(Edge, Edge)]
    """
    return self._prohibitions

  @prohibitions.setter
  def prohibitions(self, value):
    """
    Set node prohibitions
    :param value: [(Edge, Edge)]
    """
    self._prohibitions = value

  @property
  def connections(self) -> List[Connection]:
    """
    Get node connections
    :return: [Connection]
    """
    return self._connections

  @connections.setter
  def connections(self, value):
    """
    Set node connections
    :param value: [Connection]
    """
    self._connections = value
