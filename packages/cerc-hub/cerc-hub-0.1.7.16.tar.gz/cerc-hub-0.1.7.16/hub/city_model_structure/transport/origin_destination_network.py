"""
Origin-Destination network module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from typing import List
from hub.city_model_structure.network import Network
from hub.city_model_structure.transport.origin_destination_edge import OriginDestinationEdge
from hub.city_model_structure.transport.origin_destination_node import OriginDestinationNode


class OriginDestinationNetwork(Network):
  """
  OriginDestinationNetwork(Network) class
  """
  def __init__(self, name, edges=None, nodes=None):
    super().__init__(name, edges, nodes)
    self._type = "OriginDestinationNetwork"

  @property
  def type(self):
    """
    Get network type
    :return: str
    """
    return self._type

  @property
  def edges(self) -> List[OriginDestinationEdge]:
    """
    Get network edges
    :return: [OriginDestinationEdge]
    """
    return self._edges

  @property
  def nodes(self) -> List[OriginDestinationNode]:
    """
    Get network nodes
    :return: [OriginDestinationNode]
    """
    return self._nodes
