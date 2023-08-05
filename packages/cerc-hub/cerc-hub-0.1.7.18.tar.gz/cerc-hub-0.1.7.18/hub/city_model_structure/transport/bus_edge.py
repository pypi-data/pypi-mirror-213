"""
Bus edge module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from typing import List, TypeVar
from hub.city_model_structure.attributes.edge import Edge

BusNode = TypeVar('BusNode')


class BusEdge(Edge):
  """
  BusEdge class
  Each edge is unidirectional and starts at the "from" node and ends at the "to" node
  """

  def __init__(self, name, nodes, edge_type='BusEdge'):
    super().__init__(name, nodes)
    self._edge_type = edge_type
    self._average_travel_time = None

  @property
  def edge_type(self):
    """
    Get the edge type
    :return: str
    """
    return self._edge_type

  @property
  def nodes(self) -> List[BusNode]:
    """
    Get delimiting nodes for the edge
    :return: [BusNode]
    """
    return self._nodes

  @property
  def average_travel_time(self):
    """
    Add explanation here
    :return: add type of variable here
    """
    return self._average_travel_time
