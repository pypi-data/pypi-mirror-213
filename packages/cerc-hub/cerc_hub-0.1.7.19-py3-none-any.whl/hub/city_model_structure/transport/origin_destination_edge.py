"""
Origin-Destination edge module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from typing import List, TypeVar
from hub.city_model_structure.attributes.edge import Edge
from hub.city_model_structure.attributes.schedule import Schedule

OriginDestinationNode = TypeVar('OriginDestinationNode')


class OriginDestinationEdge(Edge):
  """
  OriginDestinationEdge class
  Each edge is unidirectional and starts at the "from" node and ends at the "to" node
  """

  def __init__(self, name, nodes, edge_type='OriginDestinationEdge'):
    super().__init__(name, nodes)
    self._edge_type = edge_type
    self._movement_schedule = None

  @property
  def edge_type(self):
    """
    Get the edge type
    :return: str
    """
    return self._edge_type

  @property
  def nodes(self) -> List[OriginDestinationNode]:
    """
    Get delimiting nodes for the edge
    :return: [OriginDestinationNode]
    """
    return self._nodes

  @property
  def movement_schedule(self) -> Schedule:
    """
    Get the schedule of the movement of people along this edge
    :return: Schedule
    """
    return self._movement_schedule
