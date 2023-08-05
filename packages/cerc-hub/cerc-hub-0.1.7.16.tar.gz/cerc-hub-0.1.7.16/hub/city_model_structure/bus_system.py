"""
Bus system module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from typing import List
from hub.city_model_structure.city_object import CityObject
from hub.city_model_structure.attributes.polygon import Polygon
from hub.city_model_structure.transport.bus_network import BusNetwork
from hub.city_model_structure.transport.bus_node import BusNode
from hub.city_model_structure.transport.bus import Bus


class BusSystem(CityObject):
  """
  BusSystem(CityObject) class
  """
  def __init__(self, name, surfaces):
    super().__init__(name, surfaces)
    self._bus_routes = None
    self._bus_network = None
    self._buses = None
    self._restricted_polygons = None

  @property
  def bus_routes(self) -> List[BusNode]:
    """
    Add explanation here
    :return: [BusNode]
    """
    return self._bus_routes

  @property
  def bus_network(self) -> BusNetwork:
    """
    Add explanation here
    :return: BusNetwork
    """
    return self._bus_network

  @property
  def buses(self) -> List[Bus]:
    """
    Add explanation here
    :return: [Bus]
    """
    return self._buses

  @property
  def restricted_polygons(self) -> List[Polygon]:
    """
    Add explanation here
    :return: [Polygon]
    """
    return self._restricted_polygons
