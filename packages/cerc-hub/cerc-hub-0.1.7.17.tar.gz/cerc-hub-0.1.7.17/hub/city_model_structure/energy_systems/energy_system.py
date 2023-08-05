"""
Energy system definition
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from typing import Union, List

from hub.city_model_structure.energy_systems.generation_system import GenerationSystem
from hub.city_model_structure.energy_systems.distribution_system import DistributionSystem
from hub.city_model_structure.energy_systems.emission_system import EmissionSystem
from hub.city_model_structure.energy_systems.control_system import ControlSystem
from hub.city_model_structure.city_object import CityObject


class EnergySystem:
  """
  EnergySystem class
  """
  def __init__(self):
    self._name = None
    self._demand_types = None
    self._generation_system = None
    self._distribution_system = None
    self._emission_system = None
    self._connected_city_objects = None
    self._control_system = None

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
  def generation_system(self) -> GenerationSystem:
    """
    Get generation system
    :return: GenerationSystem
    """
    return self._generation_system

  @generation_system.setter
  def generation_system(self, value):
    """
    Set generation system
    :param value: GenerationSystem
    """
    self._generation_system = value

  @property
  def distribution_system(self) -> Union[None, DistributionSystem]:
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
  def emission_system(self) -> Union[None, EmissionSystem]:
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

  @property
  def connected_city_objects(self) -> Union[None, List[CityObject]]:
    """
    Get list of city objects that are connected to this energy system
    :return: List[CityObject]
    """
    return self._connected_city_objects

  @connected_city_objects.setter
  def connected_city_objects(self, value):
    """
    Set list of city objects that are connected to this energy system
    :param value: List[CityObject]
    """
    self._connected_city_objects = value

  @property
  def control_system(self) -> Union[None, ControlSystem]:
    """
    Get control system of the energy system
    :return: ControlSystem
    """
    return self._control_system

  @control_system.setter
  def control_system(self, value):
    """
    Set control system of the energy system
    :param value: ControlSystem
    """
    self._control_system = value
