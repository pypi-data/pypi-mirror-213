"""
Crossing module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
Code contributors: Guille guille.gutierrezmorote@concordia.ca
"""

import ast
from typing import List, Union
from hub.city_model_structure.transport.traffic_node import TrafficNode


class Crossing(TrafficNode):
  """
  Crossing class
  """

  def __init__(self, name, coordinates, priority, width, shape=None, edges=None):
    super().__init__(name, coordinates, edges=edges, node_type='Crossing')
    self._priority = priority
    self._width = width
    self._shape = shape

  @property
  def priority(self) -> Union[None, bool]:
    """
    Get whether the pedestrians have priority over the vehicles
    :return: None or bool
    """
    return self._priority

  @priority.setter
  def priority(self, value):
    """
    Set whether the pedestrians have priority over the vehicles
    :param value: bool
    """
    if value is not None:
      self._priority = ast.literal_eval(value)

  @property
  def width(self) -> Union[None, float]:
    """
    Get crossing width in meters
    :return: None or float
    """
    return self._width

  @width.setter
  def width(self, value):
    """
    Set crossing width in meters
    :param value: float
    """
    if value is not None:
      self._width = float(value)

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
