"""
Origin-Destination node module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
from typing import List, TypeVar

from hub.city_model_structure.attributes.node import Node
from hub.city_model_structure.attributes.point import Point
from hub.city_model_structure.attributes.polygon import Polygon
from hub.city_model_structure.city_object import CityObject

OriginDestinationEdge = TypeVar('OriginDestinationEdge')


class OriginDestinationNode(Node):
  """
  OriginDestinationNode class
  """

  def __init__(self, name, coordinates, node_type='OriginDestinationNode', edges=None, polygon=None):
    super().__init__(name, edges)
    self._coordinates = coordinates
    self._node_type = node_type
    self._polygon = polygon
    self._land_use_types = None
    self._city_objects = None

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
  def edges(self) -> List[OriginDestinationEdge]:
    """
    get edges delimited by the node
    :return: [OriginDestinationEdge]
    """
    return self._edges

  @property
  def polygon(self) -> Polygon:
    """
    Get node polygon that defines the zone represented by the node
    :return: Polygon
    """
    return self._polygon

  @property
  def land_use_types(self) -> dict:
    """
    Get land use types inside the node polygon. It returns a dictionary with the types of land use together with the
    percentage of the land that corresponds to each type
    :return: {string : float}
    """
    return self._land_use_types

  @property
  def city_objects(self) -> List[CityObject]:
    """
    Get the list of city objects place inside the zone
    :return: List[CityObject]
    """
    return self._city_objects
