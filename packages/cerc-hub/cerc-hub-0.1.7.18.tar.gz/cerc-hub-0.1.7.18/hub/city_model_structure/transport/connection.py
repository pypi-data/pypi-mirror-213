"""
Connection module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
Code contributors: Guille guille.gutierrezmorote@concordia.ca
"""

import ast
from typing import Union

from hub.city_model_structure.attributes.edge import Edge
from hub.city_model_structure.transport.lane import Lane


class Connection:
  """
  Connection class
  """

  def __init__(self):
    self._from_edge = None
    self._to_edge = None
    self._from_lane = None
    self._to_lane = None
    self._pass = None
    self._keep_clear = None

  @property
  def from_edge(self) -> Edge:
    """
    Get "from" edge
    :return: Edge
    """
    return self._from_edge

  @from_edge.setter
  def from_edge(self, value):
    """
    Set "from" edge
    :param value: Edge
    """
    self._from_edge = value

  @property
  def to_edge(self) -> Edge:
    """
    Get "to" edge
    :return: Edge
    """
    return self._to_edge

  @to_edge.setter
  def to_edge(self, value):
    """
    Set "to" edge
    :param value: Edge
    """
    self._to_edge = value

  @property
  def from_lane(self) -> Lane:
    """
    Get "from" lane
    :return: Lane
    """
    return self._to_lane

  @from_lane.setter
  def from_lane(self, value):
    """
    Set "from" lane
    :param value: Lane
    """
    self._from_lane = value

  @property
  def to_lane(self) -> Lane:
    """
    Get "to" lane
    :return: Lane
    """
    return self._to_lane

  @to_lane.setter
  def to_lane(self, value):
    """
    Set "to" lane
    :param value: Lane
    """
    self._to_lane = value

  @property
  def pass_not_wait(self) -> Union[None, bool]:
    """
    Get if the vehicles which pass this (lane to lane) connection will not wait
    :return: None or Boolean
    """
    return self._pass

  @pass_not_wait.setter
  def pass_not_wait(self, value):
    """
    Set if the vehicles which pass this (lane to lane) connection will not wait
    :param value: Boolean
    """
    if value is not None:
      self._pass = ast.literal_eval(value)

  @property
  def keep_clear(self) -> Union[None, bool]:
    """
    Get if vehicles which pass this (lane to lane) connection should keep the intersection clear
    :return: None or Boolean
    """
    return self._keep_clear

  @keep_clear.setter
  def keep_clear(self, value):
    """
    Set if vehicles which pass this (lane to lane) connection should keep the intersection clear
    :param value: Boolean
    """
    if value is not None:
      self._keep_clear = ast.literal_eval(value)
