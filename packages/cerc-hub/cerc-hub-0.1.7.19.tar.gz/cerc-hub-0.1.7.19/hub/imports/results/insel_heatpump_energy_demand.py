"""
Insel Heap pump energy demand and fossil fuel consumption
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Concordia CERC group
Project Coder peter.yefi@gmail.cm
"""

from pathlib import Path
import pandas as pd


class InselHeatPumpEnergyDemand:
  """
  Import Energy demand and fossil fuel consumption results
  """
  def __init__(self, city, base_path, hp_model):
    """
    :param city: the city
    :param base_path: the insel simulation output file
    :param hp_model: the heatpump model for both air source and water to water
    """
    self._city = city
    self._hp_model = hp_model
    with open(Path(base_path).resolve(), 'r', encoding='utf8') as csv_file:
      df = pd.read_csv(csv_file)
    self._monthly_electricity_demand = df.iloc[:, 1]
    self._monthly_fossil_fuel_consumption = df.iloc[:, 2]

  def enrich(self):
    """
    Enrich the city with the heat pump information
    """
    for energy_system in self._city.energy_systems:
      if energy_system.air_source_hp is not None:
        if energy_system.air_source_hp.model == self._hp_model:
          energy_system.air_source_hp.hp_monthly_fossil_consumption = self._monthly_fossil_fuel_consumption

      if energy_system.water_to_water_hp is not None:
        if energy_system.water_to_water_hp.model == self._hp_model:
          energy_system.water_to_water_hp.hp_monthly_electricity_demand = self._monthly_electricity_demand
