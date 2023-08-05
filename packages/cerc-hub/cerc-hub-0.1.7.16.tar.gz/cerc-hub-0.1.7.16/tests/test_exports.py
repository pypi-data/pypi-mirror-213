"""
TestExports test and validate the city export formats
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributors: Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from pathlib import Path
from unittest import TestCase
import pandas as pd
from hub.imports.geometry_factory import GeometryFactory
from hub.helpers.dictionaries import Dictionaries
from hub.imports.construction_factory import ConstructionFactory
from hub.imports.usage_factory import UsageFactory
from hub.imports.weather_factory import WeatherFactory
from hub.exports.exports_factory import ExportsFactory
from hub.exports.energy_building_exports_factory import EnergyBuildingsExportsFactory
import hub.helpers.constants as cte
from hub.city_model_structure.city import City


class TestExports(TestCase):
  """
  TestExports class contains the unittest for export functionality
  """
  def setUp(self) -> None:
    """
    Test setup
    :return: None
    """
    self._city = None
    self._complete_city = None
    self._example_path = (Path(__file__).parent / 'tests_data').resolve()
    self._output_path = (Path(__file__).parent / 'tests_outputs').resolve()

  def _get_citygml(self, file):
    file_path = (self._example_path / file).resolve()
    self._city = GeometryFactory('citygml', path=file_path).city
    self.assertIsNotNone(self._city, 'city is none')
    return self._city

  def _get_complete_city(self, from_pickle):
    if self._complete_city is None:
      if from_pickle:
        file_path = (self._example_path / 'ConcordiaSWGcampus.pickle').resolve()
        self._complete_city = City.load(file_path)
      else:
        file_path = (self._example_path / 'one_building_in_kelowna.gml').resolve()
        self._complete_city = self._get_citygml(file_path)
        for building in self._complete_city.buildings:
          building.function = Dictionaries().hft_function_to_hub_function[building.function]
          building.year_of_construction = 2006
        ConstructionFactory('nrel', self._complete_city).enrich()
        UsageFactory('nrcan', self._complete_city).enrich()
        cli = (self._example_path / 'weather' / 'inseldb_Summerland.cli').resolve()
        self._complete_city.climate_file = Path(cli)
        self._complete_city.climate_reference_city = 'Summerland'
        dummy_measures = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for building in self._complete_city.buildings:
          building.heating_demand[cte.MONTH] = pd.DataFrame({'INSEL': dummy_measures})
          building.cooling_demand[cte.MONTH] = pd.DataFrame({'INSEL': dummy_measures})
          building.heating_demand[cte.YEAR] = pd.DataFrame({'INSEL': [0.0]})
          building.cooling_demand[cte.YEAR] = pd.DataFrame({'INSEL': [0.0]})
    return self._complete_city

  def _export(self, export_type, from_pickle=False):
    self._complete_city = self._get_complete_city(from_pickle)
    ExportsFactory(export_type, self._complete_city, self._output_path).export()

  def _export_building_energy(self, export_type, from_pickle=False):
      self._complete_city = self._get_complete_city(from_pickle)
      EnergyBuildingsExportsFactory(export_type, self._complete_city, self._output_path).export()

  def test_obj_export(self):
    """
    export to obj
    """
    self._export('obj', False)

  def test_stl_export(self):
    """
    export to stl
    """
    self._export('stl', False)

  def test_energy_ade_export(self):
    """
    export to energy ADE
    """
    self._export_building_energy('energy_ade')

  def test_sra_export(self):
    """
    export to SRA
    """
    self._export('sra')

  def test_idf_export(self):
    """
    export to IDF
    """
    file = 'FZK_Haus_LoD_2.gml'
    file_path = (self._example_path / file).resolve()
    city = GeometryFactory('citygml',
                           path=file_path,
                           function_to_hub=Dictionaries().alkis_function_to_hub_function).city
    self.assertIsNotNone(city, 'city is none')
    EnergyBuildingsExportsFactory('idf', city, self._output_path).export()
    ConstructionFactory('nrcan', city).enrich()
    EnergyBuildingsExportsFactory('idf', city, self._output_path).export()
    UsageFactory('nrcan', city).enrich()
    WeatherFactory('epw', city).enrich()
    try:
      EnergyBuildingsExportsFactory('idf', city, self._output_path).export()
    except Exception:
      self.fail("Idf ExportsFactory raised ExceptionType unexpectedly!")

