"""
AirSourceHeatPumpParameters import the heat pump information
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.comCode
contributor Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
import io

import itertools
from typing import List
from typing import Dict
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from hub.city_model_structure.energy_systems.air_source_hp import AirSourceHP
from hub.city_model_structure.energy_system import EnergySystem


class AirSourceHeatPumpParameters:
  """
  AirSourceHeatPumpParameters class
  """

  def __init__(self, city, base_path):
    self._city = city
    self._base_path = (base_path / 'heat_pumps/air_source.xlsx').resolve()

  def _read_file(self) -> Dict:
    """
    reads xlsx file containing the heat pump information
    into a dictionary
    :return : Dict
    """
    with open(self._base_path, 'rb') as xls:
      xl_file = pd.read_excel(io.BytesIO(xls.read()), sheet_name=None)

    cooling_data = {}
    heating_data = {}

    for sheet, _ in xl_file.items():
      if 'Summary' in sheet:
        continue

      # Remove nan rows and columns and extract cooling and heating data
      # for each sheet
      df = xl_file[sheet].dropna(axis=1, how='all')
      cooling_df = df.iloc[4:34, 0:8]
      heating_df = df.iloc[4:29, 8:20]

      # extract the data into dictionaries each sheet is a key entry in the
      # dictionary
      cooling_data[sheet] = {}
      heating_data[sheet] = {}
      i = 0
      # for each sheet extract data for twout/Ta.RU temperatures. Thus, the twout
      # temp is the key for the values of pf,pa,qw data
      while i < 25:
        cooling_data[sheet][cooling_df.iloc[i][0]] = cooling_df.iloc[i + 1:i + 4, 2:8].values.tolist()
        heating_data[sheet][heating_df.iloc[i][0]] = heating_df.iloc[i + 1:i + 4, 2:8].values.tolist()
        i = i + 5
      # extract the last cooling data
      cooling_data[sheet][cooling_df.iloc[i][0]] = cooling_df.iloc[i + 1:i + 4, 2:8].values.tolist()
    return {"cooling": cooling_data, "heating": heating_data}

  def enrich_city(self):
    """
    Enriches the city with information from file
    """
    heat_pump_data = self._read_file()
    for (k_cool, v_cool), (_, v_heat) in zip(heat_pump_data["cooling"].items(), heat_pump_data["heating"].items()):
      heat_pump = AirSourceHP()
      heat_pump.model = k_cool
      h_data = self._extract_heat_pump_data(v_heat)
      c_data = self._extract_heat_pump_data(v_cool)
      heat_pump.cooling_capacity = c_data[0]
      heat_pump.cooling_comp_power = c_data[1]
      heat_pump.cooling_capacity_coff = self._compute_coefficients(c_data, "cool")
      heat_pump.heating_capacity = h_data[0]
      heat_pump.heating_comp_power = h_data[1]
      heat_pump.heating_capacity_coff = self._compute_coefficients(h_data)

      energy_system = EnergySystem(f'{heat_pump.model} capacity heat pump', [])
      energy_system.air_source_hp = heat_pump
      self._city.add_city_object(energy_system)
    return self._city

  @staticmethod
  def _extract_heat_pump_data(heat_pump_capacity_data: Dict) -> [List, List]:
    """
    Fetches a list of metric based data for heat pump for various temperature,
    e.g. cooling capacity data for 12 capacity heat pump
    for 6,7,8,9,10 and 11 degree Celsius
    :param heat_pump_capacity_data: the heat pump capacity data from the
    which the metric specific data is fetched: {List}
    :return: List
    """
    cooling_heating_capacity_data = []
    compressor_power_data = []
    for _, metric_data in heat_pump_capacity_data.items():
      cooling_heating_capacity_data.append(metric_data[0])
      compressor_power_data.append(metric_data[1])
    return [cooling_heating_capacity_data, compressor_power_data]

  def _compute_coefficients(self, heat_pump_data: List, data_type="heat") -> List[float]:
    """
    Compute heat output and electrical demand coefficients
    from heating and cooling performance data
    :param heat_pump_data: a list of heat pump data. e.g. cooling capacity
    :param data_type: string to indicate if data is cooling performance data
    or heating performance data
    :return: Tuple[Dict, Dict]
    """
    # Determine the recurrence of temperature values. 6 repetitions for
    # cooling performance and 5 repetition for heating performance
    temp_multiplier = 5 if data_type == "heat" else 6
    out_temp = [25, 30, 32, 35, 40, 45] * temp_multiplier

    heat_x_values = np.repeat([-5, 0, 7, 10, 15], 6)
    cool_x_values = np.repeat([6, 7, 8, 9, 10, 11], 6)
    x_values = heat_x_values if data_type == "heat" else cool_x_values
    x_values = x_values.tolist()
    # convert list of lists to one list

    hp_data = [i / j for i, j in
               zip(list(itertools.chain.from_iterable(heat_pump_data[0])),
                   list(itertools.chain.from_iterable(heat_pump_data[1])))]

    # Compute heat output coefficients
    popt, _ = curve_fit(self._objective_function, [x_values, out_temp], hp_data)
    return popt.tolist()

  @staticmethod
  def _objective_function(xdata: List, a1: float, a2: float, a3: float, a4: float, a5: float, a6: float) -> float:
    """
    Objective function for computing coefficients
    :param xdata:
    :param a1: float
    :param a2: float
    :param a3: float
    :param a4: float
    :param a5: float
    :param a6: float
    :return:
    """
    x, y = xdata
    return (a1 * x ** 2) + (a2 * x) + (a3 * x * y) + (a4 * y) + (a5 * y ** 2) + a6
