"""
Energy System catalog equipment
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from typing import Union

from hub.catalog_factories.data_models.energy_systems.generation_system import GenerationSystem
from hub.catalog_factories.data_models.energy_systems.distribution_system import DistributionSystem
from hub.catalog_factories.data_models.energy_systems.emission_system import EmissionSystem


class System:
  """
  System class
  """
  def __init__(self,
               lod,
               system_id,
               name,
               demand_types,
               generation_system,
               distribution_system,
               emission_system):

    self._lod = lod
    self._system_id = system_id
    self._name = name
    self._demand_types = demand_types
    self._generation_system = generation_system
    self._distribution_system = distribution_system
    self._emission_system = emission_system

  @property
  def lod(self):
    """
    Get level of detail of the catalog
    :return: string
    """
    return self._lod

  @property
  def id(self):
    """
    Get equipment id
    :return: string
    """
    return self._system_id

  @property
  def name(self):
    """
    Get name
    :return: string
    """
    return f'{self._name}_lod{self._lod}'

  @property
  def demand_types(self):
    """
    Get demand able to cover from [heating, cooling, domestic_hot_water, electricity]
    :return: [string]
    """
    return self._demand_types

  @property
  def generation_system(self) -> GenerationSystem:
    """
    Get generation system
    :return: GenerationSystem
    """
    return self._generation_system

  @property
  def distribution_system(self) -> Union[None, DistributionSystem]:
    """
    Get distribution system
    :return: DistributionSystem
    """
    return self._distribution_system

  @property
  def emission_system(self) -> Union[None, EmissionSystem]:
    """
    Get emission system
    :return: EmissionSystem
    """
    return self._emission_system
