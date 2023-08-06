"""
TestSystemsFactory
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

import subprocess
from pathlib import Path
from unittest import TestCase
import copy

import hub.helpers.constants as cte
from hub.exports.energy_building_exports_factory import EnergyBuildingsExportsFactory
from hub.exports.exports_factory import ExportsFactory
from hub.helpers.dictionaries import Dictionaries
from hub.imports.construction_factory import ConstructionFactory
from hub.imports.geometry_factory import GeometryFactory
from hub.imports.weather_factory import WeatherFactory
from hub.imports.results_factory import ResultFactory
from hub.imports.usage_factory import UsageFactory
from hub.imports.energy_systems_factory import EnergySystemsFactory
from hub.city_model_structure.energy_systems.energy_system import EnergySystem
from hub.city_model_structure.energy_systems.generation_system import GenerationSystem
from hub.city_model_structure.energy_systems.distribution_system import DistributionSystem
from hub.city_model_structure.energy_systems.emission_system import EmissionSystem


class TestSystemsFactory(TestCase):
  """
  TestSystemsFactory TestCase
  """
  def setUp(self) -> None:
    """
    Test setup
    :return: None
    """
    self._example_path = (Path(__file__).parent / 'tests_data').resolve()
    self._gml_path = (self._example_path / 'FZK_Haus_LoD_2.gml').resolve()
    self._output_path = (Path(__file__).parent / 'tests_outputs').resolve()
    self._city = GeometryFactory('citygml',
                                 self._gml_path,
                                 function_to_hub=Dictionaries().alkis_function_to_hub_function).city

  def test_montreal_custom_system_factory(self):
    """
    Enrich the city with the construction information and verify it
    """
    for building in self._city.buildings:
      building.energy_systems_archetype_name = 'system 1 gas'

    EnergySystemsFactory('montreal_custom', self._city).enrich()
    self.assertEqual(1, len(self._city.energy_systems_connection_table))

  def test_montreal_custom_system_results(self):
    """
    Enrich the city with the construction information and verify it
    """
    ConstructionFactory('nrcan', self._city).enrich()
    UsageFactory('nrcan', self._city).enrich()
    WeatherFactory('epw', self._city).enrich()
    ExportsFactory('sra', self._city, self._output_path).export()
    sra_path = (self._output_path / f'{self._city.name}_sra.xml').resolve()
    subprocess.run(['sra', str(sra_path)])
    ResultFactory('sra', self._city, self._output_path).enrich()
    EnergyBuildingsExportsFactory('insel_monthly_energy_balance', self._city, self._output_path).export()
    for building in self._city.buildings:
      insel_path = (self._output_path / f'{building.name}.insel')
      subprocess.run(['insel', str(insel_path)])
    ResultFactory('insel_monthly_energy_balance', self._city, self._output_path).enrich()

    for building in self._city.buildings:
      building.energy_systems_archetype_name = 'system 1 gas pv'
    EnergySystemsFactory('montreal_custom', self._city).enrich()
    # Need to assign energy systems to buildings:
    energy_systems_connection = self._city.energy_systems_connection_table
    for building in self._city.buildings:
      _building_energy_systems = []
      energy_systems = energy_systems_connection['Energy System Type'].where(
        energy_systems_connection['Building'] == building.name
      )
      for energy_system in energy_systems:
        _generic_building_energy_systems = self._city.generic_energy_systems[energy_system]
        for _generic_building_energy_system in _generic_building_energy_systems:
          _building_energy_equipment = EnergySystem()
          _building_energy_equipment.demand_types = _generic_building_energy_system.demand_types

          _building_distribution_system = DistributionSystem()
          _building_distribution_system.generic_distribution_system = (
            copy.deepcopy(_generic_building_energy_system.distribution_system)
          )
          _building_emission_system = EmissionSystem()
          _building_emission_system.generic_emission_system = (
            copy.deepcopy(_generic_building_energy_system.emission_system)
          )
          _building_generation_system = GenerationSystem()
          _building_generation_system.generic_generation_system = (
            copy.deepcopy(_generic_building_energy_system.generation_system)
          )
          if cte.HEATING in _building_energy_equipment.demand_types:
            _building_generation_system.heat_power = building.heating_peak_load[cte.YEAR][0]
          if cte.COOLING in _building_energy_equipment.demand_types:
            _building_generation_system.cooling_power = building.cooling_peak_load[cte.YEAR][0]
          _building_energy_equipment.generation_system = _building_generation_system
          _building_energy_equipment.distribution_system = _building_distribution_system
          _building_energy_equipment.emission_system = _building_emission_system

          _building_energy_systems.append(_building_energy_equipment)
      building.energy_systems = _building_energy_systems

    for building in self._city.buildings:
      self.assertLess(0, building.heating_consumption[cte.YEAR][0])
      self.assertLess(0, building.cooling_consumption[cte.YEAR][0])
      self.assertLess(0, building.domestic_hot_water_consumption[cte.YEAR][0])
      self.assertLess(0, building.onsite_electrical_production[cte.YEAR][0])