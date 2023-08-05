"""
Montreal custom energy systems catalog module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from ast import literal_eval
import xmltodict
from hub.catalog_factories.catalog import Catalog
from hub.catalog_factories.data_models.energy_systems.system import System
from hub.catalog_factories.data_models.energy_systems.content import Content
from hub.catalog_factories.data_models.energy_systems.generation_system import GenerationSystem
from hub.catalog_factories.data_models.energy_systems.distribution_system import DistributionSystem
from hub.catalog_factories.data_models.energy_systems.emission_system import EmissionSystem
from hub.catalog_factories.data_models.energy_systems.archetype import Archetype


class MontrealCustomCatalog(Catalog):
  """
  Montreal custom energy systems catalog class
  """
  def __init__(self, path):
    path = str(path / 'montreal_custom_systems.xml')
    with open(path, 'r', encoding='utf-8') as xml:
      self._archetypes = xmltodict.parse(xml.read(), force_list=('system', 'system_cluster', 'equipment',
                                                                 'demand', 'system_id'))

    self._lod = float(self._archetypes['catalog']['@lod'])

    self._catalog_generation_equipments = self._load_generation_equipments()
    self._catalog_distribution_equipments = self._load_distribution_equipments()
    self._catalog_emission_equipments = self._load_emission_equipments()
    self._catalog_systems = self._load_systems()
    self._catalog_archetypes = self._load_archetypes()

    # store the full catalog data model in self._content
    self._content = Content(self._catalog_archetypes,
                            self._catalog_systems,
                            self._catalog_generation_equipments,
                            self._catalog_distribution_equipments,
                            self._catalog_emission_equipments)

  def _load_generation_equipments(self):
    _equipments = []
    equipments = self._archetypes['catalog']['generation_equipments']['equipment']
    for equipment in equipments:
      equipment_id = float(equipment['@id'])
      equipment_type = equipment['@type']
      fuel_type = equipment['@fuel_type']
      name = equipment['name']
      heating_efficiency = None
      if 'heating_efficiency' in equipment:
        heating_efficiency = float(equipment['heating_efficiency'])
      cooling_efficiency = None
      if 'cooling_efficiency' in equipment:
        cooling_efficiency = float(equipment['cooling_efficiency'])
      electricity_efficiency = None
      if 'electrical_efficiency' in equipment:
        electricity_efficiency = float(equipment['electrical_efficiency'])
      storage = literal_eval(equipment['storage'].capitalize())
      generation_system = GenerationSystem(equipment_id,
                                           name,
                                           equipment_type,
                                           fuel_type,
                                           None,
                                           heating_efficiency,
                                           cooling_efficiency,
                                           electricity_efficiency,
                                           None,
                                           None,
                                           storage,
                                           None)

      _equipments.append(generation_system)
    return _equipments

  def _load_distribution_equipments(self):
    _equipments = []
    equipments = self._archetypes['catalog']['distribution_equipments']['equipment']
    for equipment in equipments:
      equipment_id = float(equipment['@id'])
      equipment_type = equipment['@type']
      name = equipment['name']
      distribution_heat_losses = None
      if 'distribution_heat_losses' in equipment:
        distribution_heat_losses = float(equipment['distribution_heat_losses']['#text']) / 100
      distribution_consumption_fix_flow = None
      if 'distribution_consumption_fix_flow' in equipment:
        distribution_consumption_fix_flow = float(equipment['distribution_consumption_fix_flow']['#text']) / 100
      distribution_consumption_variable_flow = None
      if 'distribution_consumption_variable_flow' in equipment:
        distribution_consumption_variable_flow = float(equipment['distribution_consumption_variable_flow']['#text']) / 100

      distribution_system = DistributionSystem(equipment_id,
                                               name,
                                               equipment_type,
                                               None,
                                               distribution_consumption_fix_flow,
                                               distribution_consumption_variable_flow,
                                               distribution_heat_losses)

      _equipments.append(distribution_system)
    return _equipments

  def _load_emission_equipments(self):
    _equipments = []
    equipments = self._archetypes['catalog']['dissipation_equipments']['equipment']
    for equipment in equipments:
      equipment_id = float(equipment['@id'])
      equipment_type = equipment['@type']
      name = equipment['name']
      parasitic_consumption = None
      if 'parasitic_consumption' in equipment:
        parasitic_consumption = float(equipment['parasitic_consumption']['#text']) / 100

      emission_system = EmissionSystem(equipment_id,
                                       name,
                                       equipment_type,
                                       parasitic_consumption)

      _equipments.append(emission_system)
    return _equipments

  def _load_systems(self):
    _catalog_systems = []
    systems = self._archetypes['catalog']['systems']['system']
    for system in systems:
      system_id = float(system['@id'])
      name = system['name']
      demands = system['demands']['demand']
      generation_equipment = system['equipments']['generation_id']
      _generation_equipment = None
      for equipment_archetype in self._catalog_generation_equipments:
        if int(equipment_archetype.id) == int(generation_equipment):
          _generation_equipment = equipment_archetype
      distribution_equipment = system['equipments']['distribution_id']
      _distribution_equipment = None
      for equipment_archetype in self._catalog_distribution_equipments:
        if int(equipment_archetype.id) == int(distribution_equipment):
          _distribution_equipment = equipment_archetype
      emission_equipment = system['equipments']['dissipation_id']
      _emission_equipment = None
      for equipment_archetype in self._catalog_emission_equipments:
        if int(equipment_archetype.id) == int(emission_equipment):
          _emission_equipment = equipment_archetype

      _catalog_systems.append(System(self._lod,
                                     system_id,
                                     name,
                                     demands,
                                     _generation_equipment,
                                     _distribution_equipment,
                                     _emission_equipment))
    return _catalog_systems

  def _load_archetypes(self):
    _catalog_archetypes = []
    system_clusters = self._archetypes['catalog']['system_clusters']['system_cluster']
    for system_cluster in system_clusters:
      name = system_cluster['@name']
      systems = system_cluster['systems']['system_id']
      _systems = []
      for system in systems:
        for system_archetype in self._catalog_systems:
          if int(system_archetype.id) == int(system):
            _systems.append(system_archetype)
      _catalog_archetypes.append(Archetype(self._lod, name, _systems))
    return _catalog_archetypes

  def names(self, category=None):
    """
    Get the catalog elements names
    :parm: optional category filter
    """
    if category is None:
      _names = {'archetypes': [], 'systems': [], 'generation_equipments': [], 'distribution_equipments': [],
                'emission_equipments':[]}
      for archetype in self._content.archetypes:
        _names['archetypes'].append(archetype.name)
      for system in self._content.systems:
        _names['systems'].append(system.name)
      for equipment in self._content.generation_equipments:
        _names['generation_equipments'].append(equipment.name)
      for equipment in self._content.distribution_equipments:
        _names['distribution_equipments'].append(equipment.name)
      for equipment in self._content.emission_equipments:
        _names['emission_equipments'].append(equipment.name)
    else:
      _names = {category: []}
      if category.lower() == 'archetypes':
        for archetype in self._content.archetypes:
          _names[category].append(archetype.name)
      elif category.lower() == 'systems':
        for system in self._content.systems:
          _names[category].append(system.name)
      elif category.lower() == 'generation_equipments':
        for system in self._content.generation_equipments:
          _names[category].append(system.name)
      elif category.lower() == 'distribution_equipments':
        for system in self._content.distribution_equipments:
          _names[category].append(system.name)
      elif category.lower() == 'emission_equipments':
        for system in self._content.emission_equipments:
          _names[category].append(system.name)
      else:
        raise ValueError(f'Unknown category [{category}]')
    return _names

  def entries(self, category=None):
    """
    Get the catalog elements
    :parm: optional category filter
    """
    if category is None:
      return self._content
    if category.lower() == 'archetypes':
      return self._content.archetypes
    if category.lower() == 'systems':
      return self._content.systems
    if category.lower() == 'generation_equipments':
      return self._content.generation_equipments
    if category.lower() == 'distribution_equipments':
      return self._content.distribution_equipments
    if category.lower() == 'emission_equipments':
      return self._content.emission_equipments
    raise ValueError(f'Unknown category [{category}]')

  def get_entry(self, name):
    """
    Get one catalog element by names
    :parm: entry name
    """
    for entry in self._content.archetypes:
      if entry.name.lower() == name.lower():
        return entry
    for entry in self._content.systems:
      if entry.name.lower() == name.lower():
        return entry
    for entry in self._content.generation_equipments:
      if entry.name.lower() == name.lower():
        return entry
    for entry in self._content.distribution_equipments:
      if entry.name.lower() == name.lower():
        return entry
    for entry in self._content.emission_equipments:
      if entry.name.lower() == name.lower():
        return entry
    raise IndexError(f"{name} doesn't exists in the catalog")
