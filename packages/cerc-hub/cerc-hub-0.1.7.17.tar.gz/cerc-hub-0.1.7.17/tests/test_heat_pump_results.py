"""
Test EnergySystemsFactory and various heatpump models
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""
from unittest import TestCase
from hub.imports.geometry_factory import GeometryFactory
from hub.imports.energy_systems_factory import EnergySystemsFactory
from hub.exports.energy_systems_factory import EnergySystemsExportFactory
from hub.imports.results_factory import ResultFactory
import os
from pandas.core.series import Series

# User defined parameters
user_input = {
  'StartYear': 2020,
  'EndYear': 2021,
  'MaximumHPEnergyInput': 8000,
  'HoursOfStorageAtMaxDemand': 1,
  'BuildingSuppTemp': 40,
  'TemperatureDifference': 15,
  'FuelLHV': 47100,
  'FuelPrice': 0.12,
  'FuelEF': 1887,
  'FuelDensity': 0.717,
  'HPSupTemp': 60
}


class TestHeatPumpResults(TestCase):
  """
  TestHeatPumpResults
  """

  def setUp(self) -> None:
    """
    Test setup
    :return: None
    """
    city_file = "tests_data/C40_Final.gml"
    self._output_path = "tests_data/as_user_output.csv"
    self._city = GeometryFactory('citygml', path=city_file).city
    EnergySystemsFactory('air_source_hp', self._city).enrich()

  def test_air_source_series_heat_pump_012_results(self):
    EnergySystemsExportFactory(city=self._city, handler=user_input, hp_model='012',
                               output_path=self._output_path).export()
    ResultFactory('heat_pump', self._city, self._output_path, '012').enrich()

    for energy_system in self._city.energy_systems:
      self.assertIsNone(energy_system.water_to_water_hp)
      if energy_system.air_source_hp.model == '012':
        self.assertIsInstance(energy_system.air_source_hp.hp_monthly_fossil_consumption, Series)
        self.assertEqual(energy_system.air_source_hp.hp_monthly_fossil_consumption.iloc[5], 1.51325583)
        self.assertEqual(energy_system.air_source_hp.hp_monthly_fossil_consumption.iloc[12], 35.853598782915)

  def test_air_source_series_heat_pump_015_results(self):
    EnergySystemsExportFactory(city=self._city, handler=user_input, hp_model='140',
                               output_path=self._output_path).export()
    ResultFactory('heat_pump', self._city, self._output_path, '140').enrich()

    for energy_system in self._city.energy_systems:
      self.assertIsNone(energy_system.water_to_water_hp)
      if energy_system.air_source_hp.model == '140':
        self.assertIsInstance(energy_system.air_source_hp.hp_monthly_fossil_consumption, Series)
        self.assertEqual(energy_system.air_source_hp.hp_monthly_fossil_consumption.iloc[0], 7.91282225)
        self.assertEqual(energy_system.air_source_hp.hp_monthly_fossil_consumption.iloc[2], 0.068873927)

  def tearDown(self) -> None:
    try:
      os.remove(self._output_path)
    except OSError:
      pass
