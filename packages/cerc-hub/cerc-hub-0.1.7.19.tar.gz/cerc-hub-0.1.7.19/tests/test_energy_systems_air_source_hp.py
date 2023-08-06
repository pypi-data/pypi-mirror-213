"""
Test EnergySystemsFactory and various heatpump models
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""
import pandas as pd
from unittest import TestCase
from hub.imports.geometry_factory import GeometryFactory
from hub.imports.energy_systems_factory import EnergySystemsFactory
from hub.city_model_structure.energy_systems.air_source_hp import AirSourceHP
from hub.exports.energy_systems_factory import EnergySystemsExportFactory
import os

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


class TestEnergySystemsFactory(TestCase):
  """
  TestBuilding TestCase 1
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

  def test_air_source_heat_pump_import(self):
    self.assertIsNotNone(self._city.energy_systems, 'City has energy systems')
    self.assertIsInstance(self._city.energy_systems[0].air_source_hp, AirSourceHP)
    self.assertEqual(self._city.energy_systems[0].air_source_hp.model, '012')
    self.assertEqual(self._city.energy_systems[16].air_source_hp.model, '140')

  def test_air_source_series_heat_pump_export(self):
    EnergySystemsExportFactory(city=self._city, handler=user_input, hp_model='012',
                               output_path=self._output_path).export()
    df = pd.read_csv(self._output_path)
    self.assertEqual(df.shape, (13, 3))
    self.assertEqual(df.iloc[0, 1], 1867715.88)

  def test_air_source_parallel_heat_pump_export(self):
    output = EnergySystemsExportFactory(city=self._city, handler=user_input, hp_model='018',
                                        output_path=None, sim_type=1).export()
    self.assertEqual(output["hourly_electricity_demand"][0], 38748.5625)
    self.assertIsNotNone(output["daily_fossil_consumption"])
    self.assertEqual(len(output["hourly_electricity_demand"]), 8760)

  def tearDown(self) -> None:
    try:
      os.remove(self._output_path)
    except OSError:
      pass
