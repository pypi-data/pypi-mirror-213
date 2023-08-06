"""
Walkway node module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
Code contributors: Guille guille.gutierrezmorote@concordia.ca
"""

from typing import List, Union
from hub.city_model_structure.transport.traffic_node import TrafficNode


class WalkwayNode(TrafficNode):
  """
  WalkwayNode class
  """

  def __init__(self, name, coordinates, edges=None, shape=None):
    super().__init__(name, coordinates, edges=edges, node_type='WalkwayNode')
    self._shape = shape

  @property
  def shape(self) -> Union[None, List[List[float]]]:
    """
    Get the list of positions
    :return: None or [[x, y, (z)]]
    """
    return self._shape

  @shape.setter
  def shape(self, value):
    """
    Set the list of positions
    :param value: [[x, y, (z)]]
    """
    if value is not None:
      self._shape = [[float(i) for i in value]]
