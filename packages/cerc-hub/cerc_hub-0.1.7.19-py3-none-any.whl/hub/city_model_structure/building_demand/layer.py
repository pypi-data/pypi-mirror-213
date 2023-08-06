"""
Layers module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
"""
import uuid
from typing import Union
from hub.city_model_structure.building_demand.material import Material


class Layer:
  """
  Layer class
  """
  def __init__(self):
    self._material = None
    self._thickness = None
    self._id = None

  @property
  def id(self):
    """
    Get layer id, a universally unique identifier randomly generated
    :return: str
    """
    if self._id is None:
      self._id = uuid.uuid4()
    return self._id

  @property
  def material(self) -> Material:
    """
    Get layer material
    :return: Material
    """
    return self._material

  @material.setter
  def material(self, value):
    """
    Set layer material
    :param value: Material
    """
    self._material = value

  @property
  def thickness(self) -> Union[None, float]:
    """
    Get layer thickness in meters
    :return: None or float
    """
    return self._thickness

  @thickness.setter
  def thickness(self, value):
    """
    Get layer thickness in meters
    :param value: float
    """
    if value is not None:
      self._thickness = float(value)
