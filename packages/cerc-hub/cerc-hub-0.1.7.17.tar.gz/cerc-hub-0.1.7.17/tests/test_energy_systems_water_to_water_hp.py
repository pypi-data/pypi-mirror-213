"""
Test EnergySystemsFactory and various heatpump models
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""
from unittest import TestCase

import pandas as pd

from hub.city_model_structure.energy_systems.water_to_water_hp import WaterToWaterHP
from hub.exports.energy_systems_factory import EnergySystemsExportFactory
from hub.imports.energy_systems_factory import EnergySystemsFactory
from hub.imports.geometry_factory import GeometryFactory


class TestEnergySystemsFactory(TestCase):
  """
  TestEnergySystemsFactory for Water to Water HP
  """

  def setUp(self) -> None:
    """
    Test setup
    :return: None
    """
    city_file = "tests_data/C40_Final.gml"
    self._output_path = "tests_data/w2w_user_output.csv"
    self._city = GeometryFactory('citygml', path=city_file).city
    EnergySystemsFactory('water_to_water_hp', self._city).enrich()

  def test_water_to_water_heat_pump_import(self):
    self.assertIsNotNone(self._city.energy_systems, 'City has energy systems')
    self.assertIsInstance(self._city.energy_systems[0].water_to_water_hp, WaterToWaterHP)
    self.assertEqual(self._city.energy_systems[0].water_to_water_hp.model, 'ClimateMaster 156 kW')
    self.assertEqual(self._city.energy_systems[2].water_to_water_hp.model, 'ClimateMaster 335 kW')

  def test_water_to_water_heat_pump_export(self):
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
      'HPSupTemp': 60,
      'b1': 10,
      'b2': 10,
      'b3': 10,
      'b4': 10,
      'b5': 10,
      'b6': 10,
      'b7': 10,
      'b8': 10,
      'b9': 10,
      'b10': 10,
      'b11': 10
    }

    EnergySystemsExportFactory(city=self._city, handler=user_input, hp_model='ClimateMaster 256 kW',
                               output_path=self._output_path, sim_type=1).export('water')
    df = pd.read_csv(self._output_path)
    self.assertEqual(df.shape, (13, 3))
    self.assertEqual(df.iloc[0, 1], 1031544.62)
