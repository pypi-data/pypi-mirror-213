"""
Generic energy system definition
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from typing import Union

from hub.city_model_structure.energy_systems.generic_distribution_system import GenericDistributionSystem
from hub.city_model_structure.energy_systems.generic_emission_system import GenericEmissionSystem
from hub.city_model_structure.energy_systems.generic_generation_system import GenericGenerationSystem


class GenericEnergySystem:
  """
  GenericEnergySystem class
  """
  def __init__(self):
    self._name = None
    self._demand_types = None
    self._generation_system = None
    self._distribution_system = None
    self._emission_system = None
    self._connected_city_objects = None

  @property
  def name(self):
    """
    Get energy system name
    :return: str
    """
    return self._name

  @name.setter
  def name(self, value):
    """
    Set energy system name
    :param value:
    """
    self._name = value

  @property
  def demand_types(self):
    """
    Get demand able to cover from [Heating, Cooling, Domestic Hot Water, Electricity]
    :return: [string]
    """
    return self._demand_types

  @demand_types.setter
  def demand_types(self, value):
    """
    Set demand able to cover from [Heating, Cooling, Domestic Hot Water, Electricity]
    :param value: [string]
    """
    self._demand_types = value

  @property
  def generation_system(self) -> GenericGenerationSystem:
    """
    Get generation system
    :return: GenerationSystem
    """
    return self._generation_system

  @generation_system.setter
  def generation_system(self, value):
    """
    Set generation system
    :return: GenerationSystem
    """
    self._generation_system = value

  @property
  def distribution_system(self) -> Union[None, GenericDistributionSystem]:
    """
    Get distribution system
    :return: DistributionSystem
    """
    return self._distribution_system

  @distribution_system.setter
  def distribution_system(self, value):
    """
    Set distribution system
    :param value: DistributionSystem
    """
    self._distribution_system = value

  @property
  def emission_system(self) -> Union[None, GenericEmissionSystem]:
    """
    Get emission system
    :return: EmissionSystem
    """
    return self._emission_system

  @emission_system.setter
  def emission_system(self, value):
    """
    Set emission system
    :param value: EmissionSystem
    """
    self._emission_system = value
