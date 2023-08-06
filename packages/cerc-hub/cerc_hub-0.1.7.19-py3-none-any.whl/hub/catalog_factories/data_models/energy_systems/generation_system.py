"""
Energy System catalog generation system
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from __future__ import annotations
from typing import Union


class GenerationSystem:
  """
  Generation system class
  """
  def __init__(self, system_id, name, system_type, fuel_type, source_types, heat_efficiency, cooling_efficiency,
               electricity_efficiency, source_temperature, source_mass_flow, storage, auxiliary_equipment):

    self._system_id = system_id
    self._name = name
    self._type = system_type
    self._fuel_type = fuel_type
    self._source_types = source_types
    self._heat_efficiency = heat_efficiency
    self._cooling_efficiency = cooling_efficiency
    self._electricity_efficiency = electricity_efficiency
    self._source_temperature = source_temperature
    self._source_mass_flow = source_mass_flow
    self._storage = storage
    self._auxiliary_equipment = auxiliary_equipment

  @property
  def id(self):
    """
    Get system id
    :return: float
    """
    return self._system_id

  @id.setter
  def id(self, value):
    """
    Set system id
    :param value: float
    """
    self._system_id = value

  @property
  def name(self):
    """
    Get name
    :return: string
    """
    return self._name

  @name.setter
  def name(self, value):
    """
    Set name
    :param value: string
    """
    self._name = value

  @property
  def type(self):
    """
    Get type
    :return: string
    """
    return self._type

  @property
  def fuel_type(self):
    """
    Get fuel_type from [renewable, gas, diesel, electricity, wood, coal]
    :return: string
    """
    return self._fuel_type

  @property
  def source_types(self):
    """
    Get source_type from [air, water, geothermal, district_heating, grid, on_site_electricity]
    :return: [string]
    """
    return self._source_types

  @property
  def heat_efficiency(self):
    """
    Get heat_efficiency
    :return: float
    """
    return self._heat_efficiency

  @property
  def cooling_efficiency(self):
    """
    Get cooling_efficiency
    :return: float
    """
    return self._cooling_efficiency

  @property
  def electricity_efficiency(self):
    """
    Get electricity_efficiency
    :return: float
    """
    return self._electricity_efficiency

  @property
  def source_temperature(self):
    """
    Get source_temperature in degree Celsius
    :return: float
    """
    return self._source_temperature

  @property
  def source_mass_flow(self):
    """
    Get source_mass_flow in kg/s
    :return: float
    """
    return self._source_mass_flow

  @property
  def storage(self):
    """
    Get boolean storage exists
    :return: bool
    """
    return self._storage

  @property
  def auxiliary_equipment(self) -> Union[None, GenerationSystem]:
    """
    Get auxiliary_equipment
    :return: GenerationSystem
    """
    return self._auxiliary_equipment
