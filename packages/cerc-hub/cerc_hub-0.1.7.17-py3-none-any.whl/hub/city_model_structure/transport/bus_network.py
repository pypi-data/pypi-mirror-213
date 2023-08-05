"""
Bus network module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from typing import List
from hub.city_model_structure.network import Network
from hub.city_model_structure.transport.bus_edge import BusEdge
from hub.city_model_structure.transport.bus_node import BusNode


class BusNetwork(Network):
  """
  BusNetwork(Network) class
  """
  def __init__(self, name, edges=None, nodes=None):
    super().__init__(name, edges, nodes)
    self._type = "BusNetwork"

  @property
  def type(self):
    """
    Get network type
    :return: str
    """
    return self._type

  @property
  def edges(self) -> List[BusEdge]:
    """
    Get network edges
    :return: [BusEdge]
    """
    return self._edges

  @property
  def nodes(self) -> List[BusNode]:
    """
    Get network nodes
    :return: [BusNode]
    """
    return self._nodes
