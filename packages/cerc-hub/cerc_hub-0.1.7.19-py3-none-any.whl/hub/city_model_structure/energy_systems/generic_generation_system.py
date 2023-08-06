"""
Generic energy generation system definition
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from __future__ import annotations
from typing import Union


class GenericGenerationSystem:
  """
  GenericGenerationSystem class
  """
  def __init__(self):
    self._type = None
    self._fuel_type = None
    self._source_types = None
    self._heat_efficiency = None
    self._cooling_efficiency = None
    self._electricity_efficiency = None
    self._source_temperature = None
    self._source_mass_flow = None
    self._storage = None
    self._auxiliary_equipment = None

  @property
  def type(self):
    """
    Get system type
    :return: string
    """
    return self._type

  @type.setter
  def type(self, value):
    """
    Set system type
    :param value: string
    """
    self._type = value

  @property
  def fuel_type(self):
    """
    Get fuel_type from [Renewable, Gas, Diesel, Electricity, Wood, Coal]
    :return: string
    """
    return self._fuel_type

  @fuel_type.setter
  def fuel_type(self, value):
    """
    Set fuel_type from [Renewable, Gas, Diesel, Electricity, Wood, Coal]
    :param value: string
    """
    self._fuel_type = value

  @property
  def source_types(self):
    """
    Get source_type from [Air, Water, Geothermal, District Heating, Grid, Onsite Electricity]
    :return: [string]
    """
    return self._source_types

  @source_types.setter
  def source_types(self, value):
    """
    Set source_type from [Air, Water, Geothermal, District Heating, Grid, Onsite Electricity]
    :param value: [string]
    """
    self._source_types = value

  @property
  def heat_efficiency(self):
    """
    Get heat_efficiency
    :return: float
    """
    return self._heat_efficiency

  @heat_efficiency.setter
  def heat_efficiency(self, value):
    """
    Set heat_efficiency
    :param value: float
    """
    self._heat_efficiency = value

  @property
  def cooling_efficiency(self):
    """
    Get cooling_efficiency
    :return: float
    """
    return self._cooling_efficiency

  @cooling_efficiency.setter
  def cooling_efficiency(self, value):
    """
    Set cooling_efficiency
    :param value: float
    """
    self._cooling_efficiency = value

  @property
  def electricity_efficiency(self):
    """
    Get electricity_efficiency
    :return: float
    """
    return self._electricity_efficiency

  @electricity_efficiency.setter
  def electricity_efficiency(self, value):
    """
    Set electricity_efficiency
    :param value: float
    """
    self._electricity_efficiency = value

  @property
  def source_temperature(self):
    """
    Get source_temperature in degree Celsius
    :return: float
    """
    return self._source_temperature

  @source_temperature.setter
  def source_temperature(self, value):
    """
    Set source_temperature in degree Celsius
    :param value: float
    """
    self._source_temperature = value

  @property
  def source_mass_flow(self):
    """
    Get source_mass_flow in kg/s
    :return: float
    """
    return self._source_mass_flow

  @source_mass_flow.setter
  def source_mass_flow(self, value):
    """
    Set source_mass_flow in kg/s
    :param value: float
    """
    self._source_mass_flow = value

  @property
  def storage(self):
    """
    Get boolean storage exists
    :return: bool
    """
    return self._storage

  @storage.setter
  def storage(self, value):
    """
    Set boolean storage exists
    :return: bool
    """
    self._storage = value

  @property
  def auxiliary_equipment(self) -> Union[None, GenericGenerationSystem]:
    """
    Get auxiliary_equipment
    :return: GenerationSystem
    """
    return self._auxiliary_equipment

  @auxiliary_equipment.setter
  def auxiliary_equipment(self, value):
    """
    Set auxiliary_equipment
    :return: GenerationSystem
    """
    self._auxiliary_equipment = value
