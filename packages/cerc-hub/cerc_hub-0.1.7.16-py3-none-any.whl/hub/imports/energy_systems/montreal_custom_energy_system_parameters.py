"""
Montreal custom energy system importer
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

import logging
import copy

from pandas import DataFrame

from hub.catalog_factories.energy_systems_catalog_factory import EnergySystemsCatalogFactory
from hub.city_model_structure.energy_systems.generic_distribution_system import GenericDistributionSystem
from hub.city_model_structure.energy_systems.generic_energy_system import GenericEnergySystem
from hub.city_model_structure.energy_systems.generic_generation_system import GenericGenerationSystem
from hub.city_model_structure.energy_systems.energy_system import EnergySystem
from hub.city_model_structure.energy_systems.generation_system import GenerationSystem
from hub.city_model_structure.energy_systems.distribution_system import DistributionSystem
from hub.city_model_structure.energy_systems.emission_system import EmissionSystem
from hub.helpers.dictionaries import Dictionaries


class MontrealCustomEnergySystemParameters:
  """
  MontrealCustomEnergySystemParameters class
  """

  def __init__(self, city):
    self._city = city

  def enrich_buildings(self):
    """
    Returns the city with the system parameters assigned to the buildings
    :return:
    """
    city = self._city
    montreal_custom_catalog = EnergySystemsCatalogFactory('montreal_custom').catalog
    if city.energy_systems_connection_table is None:
      _energy_systems_connection_table = DataFrame(columns=['Energy System Type', 'Building'])
    else:
      _energy_systems_connection_table = city.energy_systems_connection_table
    if city.generic_energy_systems is None:
      _generic_energy_systems = {}
    else:
      _generic_energy_systems = city.generic_energy_systems
    for building in city.buildings:
      archetype_name = f'{building.energy_systems_archetype_name}_lod1.0'
      try:
        archetype = self._search_archetypes(montreal_custom_catalog, archetype_name)
      except KeyError:
        logging.error('Building %s has unknown energy system archetype for system name %s', building.name,
                      archetype_name)
        continue

      _energy_systems_connection_table, _generic_energy_systems \
        = self._create_generic_systems(archetype, building,
                                       _energy_systems_connection_table, _generic_energy_systems)

    city.energy_systems_connection_table = _energy_systems_connection_table
    city.generic_energy_systems = _generic_energy_systems

    self._associate_energy_systems(city)

  @staticmethod
  def _search_archetypes(catalog, name):
    archetypes = catalog.entries('archetypes')
    for building_archetype in archetypes:
      if str(name) == str(building_archetype.name):
        return building_archetype
    raise KeyError('archetype not found')

  @staticmethod
  def _create_generic_systems(archetype, building,
                              _energy_systems_connection_table, _generic_energy_systems):
    building_systems = []
    data = [archetype.name, building.name]
    _energy_systems_connection_table.loc[len(_energy_systems_connection_table)] = data
    for system in archetype.systems:
      energy_system = GenericEnergySystem()
      _hub_demand_types = []
      for demand_type in system.demand_types:
        _hub_demand_types.append(Dictionaries().montreal_demand_type_to_hub_energy_demand_type[demand_type])
      energy_system.name = system.name
      energy_system.demand_types = _hub_demand_types
      _generation_system = GenericGenerationSystem()
      archetype_generation_equipment = system.generation_system
      _type = str(system.name).split('_', maxsplit=1)[0]
      _generation_system.type = Dictionaries().montreal_system_to_hub_energy_generation_system[
        _type]
      _generation_system.fuel_type = archetype_generation_equipment.fuel_type
      _generation_system.source_types = archetype_generation_equipment.source_types
      _generation_system.heat_efficiency = archetype_generation_equipment.heat_efficiency
      _generation_system.cooling_efficiency = archetype_generation_equipment.cooling_efficiency
      _generation_system.electricity_efficiency = archetype_generation_equipment.electricity_efficiency
      _generation_system.source_temperature = archetype_generation_equipment.source_temperature
      _generation_system.source_mass_flow = archetype_generation_equipment.source_mass_flow
      _generation_system.storage = archetype_generation_equipment.storage
      _generation_system.auxiliary_equipment = None

      energy_system.generation_system = _generation_system

      _distribution_system = GenericDistributionSystem()
      archetype_distribution_equipment = system.distribution_system
      _distribution_system.type = archetype_distribution_equipment.type
      _distribution_system.supply_temperature = archetype_distribution_equipment.supply_temperature
      _distribution_system.distribution_consumption_fix_flow = \
        archetype_distribution_equipment.distribution_consumption_fix_flow
      _distribution_system.distribution_consumption_variable_flow = \
        archetype_distribution_equipment.distribution_consumption_variable_flow
      _distribution_system.heat_losses = archetype_distribution_equipment.heat_losses

      energy_system.distribution_system = _distribution_system

      building_systems.append(energy_system)
    if archetype.name not in _generic_energy_systems:
      _generic_energy_systems[archetype.name] = building_systems

    return _energy_systems_connection_table, _generic_energy_systems

  @staticmethod
  def _associate_energy_systems(city):
    energy_systems_connection = city.energy_systems_connection_table
    for building in city.buildings:
      _building_energy_systems = []
      energy_systems = energy_systems_connection['Energy System Type'] \
        .where(energy_systems_connection['Building'] == building.name)
      for energy_system in energy_systems:
        _generic_building_energy_systems = city.generic_energy_systems[energy_system]
        for _generic_building_energy_system in _generic_building_energy_systems:
          _building_energy_equipment = EnergySystem()
          _building_energy_equipment.name = _generic_building_energy_system.name
          _building_energy_equipment.demand_types = _generic_building_energy_system.demand_types

          _building_distribution_system = DistributionSystem()
          _building_distribution_system.generic_distribution_system = \
            copy.deepcopy(_generic_building_energy_system.distribution_system)
          _building_emission_system = EmissionSystem()
          _building_emission_system.generic_emission_system = \
            copy.deepcopy(_generic_building_energy_system.emission_system)
          _building_generation_system = GenerationSystem()
          _building_generation_system.generic_generation_system = \
            copy.deepcopy(_generic_building_energy_system.generation_system)

          _building_energy_equipment.generation_system = _building_generation_system
          _building_energy_equipment.distribution_system = _building_distribution_system
          _building_energy_equipment.emission_system = _building_emission_system

          _building_energy_systems.append(_building_energy_equipment)
      building.energy_systems = _building_energy_systems
