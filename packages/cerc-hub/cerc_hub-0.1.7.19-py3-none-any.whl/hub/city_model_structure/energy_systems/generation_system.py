"""
Energy generation system definition
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from __future__ import annotations
from typing import Union

from hub.city_model_structure.energy_systems.generic_generation_system import GenericGenerationSystem


class GenerationSystem:
  """
  GenerationSystem class
  """
  def __init__(self):
    self._heat_power = None
    self._cooling_power = None
    self._electricity_power = None
    self._storage_capacity = None
    self._generic_generation_system = None
    self._auxiliary_equipment = None

  @property
  def generic_generation_system(self) -> GenericGenerationSystem:
    """
    Get associated generic_generation_system
    :return: GenericGenerationSystem
    """
    return self._generic_generation_system

  @generic_generation_system.setter
  def generic_generation_system(self, value):
    """
    Set associated generic_generation_system
    :param value: GenericGenerationSystem
    """
    self._generic_generation_system = value

  @property
  def heat_power(self):
    """
    Get heat_power in W
    :return: float
    """
    return self._heat_power

  @heat_power.setter
  def heat_power(self, value):
    """
    Set heat_power in W
    :param value: float
    """
    self._heat_power = value

  @property
  def cooling_power(self):
    """
    Get cooling_power in W
    :return: float
    """
    return self._cooling_power

  @cooling_power.setter
  def cooling_power(self, value):
    """
    Set cooling_power in W
    :param value: float
    """
    self._cooling_power = value

  @property
  def electricity_power(self):
    """
    Get electricity_power in W
    :return: float
    """
    return self._electricity_power

  @electricity_power.setter
  def electricity_power(self, value):
    """
    Set electricity_power in W
    :param value: float
    """
    self._electricity_power = value

  @property
  def storage_capacity(self):
    """
    Get storage_capacity in J
    :return: float
    """
    return self._storage_capacity

  @storage_capacity.setter
  def storage_capacity(self, value):
    """
    Set storage_capacity in J
    :param value: float
    """
    self._storage_capacity = value

  @property
  def auxiliary_equipment(self) -> Union[None, GenerationSystem]:
    """
    Get auxiliary_equipment
    :return: GenerationSystem
    """
    return self._auxiliary_equipment

  @auxiliary_equipment.setter
  def auxiliary_equipment(self, value):
    """
    Set auxiliary_equipment
    :param value: GenerationSystem
    """
    self._auxiliary_equipment = value
