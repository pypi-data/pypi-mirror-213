"""
Traffic network module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
Code contributors: Guille guille.gutierrezmorote@concordia.ca
"""

from typing import List
from hub.city_model_structure.network import Network
from hub.city_model_structure.transport.traffic_edge import TrafficEdge
from hub.city_model_structure.transport.traffic_node import TrafficNode


class TrafficNetwork(Network):
  """
  TrafficNetwork(Network) class
  """
  def __init__(self, name, edges=None, nodes=None):
    super().__init__(name, edges, nodes)
    self._type = "TrafficNetwork"

  @property
  def type(self):
    """
    Get network type
    :return: str
    """
    return self._type

  @property
  def edges(self) -> List[TrafficEdge]:
    """
    Get network edges
    :return: [TrafficEdge]
    """
    return self._edges

  @property
  def nodes(self) -> List[TrafficNode]:
    """
    Get network nodes
    :return: [TrafficNode]
    """
    return self._nodes
