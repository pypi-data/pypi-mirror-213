"""
WaterToWaterHPParameters import the heat pump information
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""

from typing import Dict
from typing import List

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

from hub.city_model_structure.energy_system import EnergySystem
from hub.city_model_structure.energy_systems.water_to_water_hp import WaterToWaterHP


class WaterToWaterHPParameters:
  """
  WaterToWaterHPParameters class
  """

  def __init__(self, city, base_path):
    self._city = city
    self._base_path = (base_path / 'heat_pumps/water_to_water.xlsx').resolve()

  def _read_file(self) -> Dict:
    # todo: this method is keeping the excel file open and should be either corrected or removed
    xl_file = pd.ExcelFile(self._base_path)
    heat_pump_dfs = {sheet_name: xl_file.parse(sheet_name)
                     for sheet_name in xl_file.sheet_names}

    hp_data = {}
    flow_rates = {
      '156': [2.84, 4.23, 5.68],
      '256': [4.73, 7.13, 9.446],
      '335': [6.62, 9.97, 12.93],
    }

    for sheet, _ in heat_pump_dfs.items():

      df = heat_pump_dfs[sheet].dropna(axis=1, how='all')
      df = df.iloc[3:, 6:35]

      if '156' in sheet:
        hp_data[sheet] = self._extract_required_hp_data(df, [0, 10, 25, 40, 55, 67], flow_rates['156'])
      elif '256' in sheet:
        hp_data[sheet] = self._extract_required_hp_data(df, [0, 9, 24, 39, 54, 66], flow_rates['256'])
      elif '335' in sheet:
        hp_data[sheet] = self._extract_required_hp_data(df, [0, 11, 26, 41, 56, 69], flow_rates['335'])

    return hp_data

  def _extract_required_hp_data(self, dataframe, ranges, flow_rates):
    """
    Extracts 156 Kw water to water heat pump data
    :param dataframe: dataframe containing all data
    :param ranges: the range of values to extract
    :param flow_rates: the flow rates of water through pump
    :return: Dict
    """
    # extract data rows and columns
    data = {'tc': self._extract_hp_data(dataframe, [1, 11, 21], ranges),
            'pd': self._extract_hp_data(dataframe, [2, 12, 22], ranges),
            'lwt': self._extract_hp_data(dataframe, [5, 15, 25], ranges),
            'fr': (self._extract_flow_and_ewt(dataframe, ranges, [1, 11, 21], flow_rates))[0],
            'ewt': (self._extract_flow_and_ewt(dataframe, ranges, [1, 11, 21], flow_rates))[1]}
    # range values for extracting data
    return data

  @staticmethod
  def _extract_hp_data(df, columns, ranges):
    """
    Extract variable specific (LWT, PD or TC) data from water to water hp
    :param df: the dataframe
    :param columns: the columns to extract data from
    :param ranges: the range of values to extract
    :return: List
    """
    data = pd.concat([df.iloc[ranges[0]:ranges[1], columns[0]], df.iloc[ranges[0]:ranges[1], columns[1]]])
    data = pd.concat([df.iloc[ranges[0]:ranges[1], columns[2]], data])
    for i in range(1, 5):
      data = pd.concat([df.iloc[ranges[i]:ranges[i + 1], columns[0]], data])
      data = pd.concat([df.iloc[ranges[i]:ranges[i + 1], columns[1]], data])
      data = pd.concat([df.iloc[ranges[i]:ranges[i + 1], columns[2]], data])

    return data.dropna().values.tolist()

  @staticmethod
  def _extract_flow_and_ewt(df, ranges, columns, flow_rates):
    """
    Create the flow and ewt data based on the length of the various
    columns for the variables being extracted
    :param df: the dataframe
    :param ranges: the range of values to extract
    :param columns: the columns to extract data from
    :param flow_rates: flow rate values
    :return:
    """
    ewt_values = [-1.111111111, 4.444444444, 10, 15.55555556, 21.11111111]
    length = [len(df.iloc[ranges[0]:ranges[1], columns[0]].dropna()),
              len(df.iloc[ranges[0]:ranges[1], columns[1]].dropna()),
              len(df.iloc[ranges[0]:ranges[1], columns[2]].dropna())]

    ewt_data = np.repeat(ewt_values[0], sum(length))
    flow_rates_data = np.repeat(flow_rates, length)

    for i in range(1, 5):
      length = [len(df.iloc[ranges[i]:ranges[i + 1], columns[0]].dropna()),
                len(df.iloc[ranges[i]:ranges[i + 1], columns[1]].dropna()),
                len(df.iloc[ranges[i]:ranges[i + 1], columns[2]].dropna())]
      flow_rates_data = np.append(flow_rates_data, np.repeat(flow_rates, length))
      ewt_data = np.append(ewt_data, np.repeat(ewt_values[i], sum(length)))

    return flow_rates_data.tolist(), ewt_data.tolist()

  def enrich_city(self):
    """
    Enriches the city with information from file
    """
    heap_pump_data = self._read_file()
    for model, data in heap_pump_data.items():
      heat_pump = WaterToWaterHP()
      heat_pump.model = model.strip()
      heat_pump.total_cooling_capacity = data['tc']
      heat_pump.power_demand = data['pd']
      heat_pump.flow_rate = data['fr']
      heat_pump.entering_water_temp = data['ewt']
      heat_pump.leaving_water_temp = data['lwt']
      heat_pump.power_demand_coff = self._compute_coefficients(data)
      energy_system = EnergySystem(heat_pump.model, [])
      energy_system.water_to_water_hp = heat_pump
      self._city.add_city_object(energy_system)
    return self._city

  def _compute_coefficients(self, heat_pump_data: Dict) -> List[float]:
    """
    Compute heat output and electrical demand coefficients
    from heating performance data
    :param heat_pump_data: a dictionary of heat pump data.
    :return: Tuple[Dict, Dict]
    """
    demand = [i / j for i, j in zip(heat_pump_data['tc'], heat_pump_data['pd'])]

    # Compute heat output coefficients
    popt, _ = curve_fit(
      self._objective_function, [heat_pump_data['ewt'], heat_pump_data['lwt'], heat_pump_data['fr']], demand
    )
    return popt.tolist()

  @staticmethod
  def _objective_function(xdata: List, a1: float, a2: float, a3: float, a4: float, a5: float, a6: float,
                          a7: float, a8: float, a9: float, a10: float, a11: float) -> float:
    """
    Objective function for computing coefficients
    :param xdata:
    :param a1: float
    :param a2: float
    :param a3: float
    :param a4: float
    :param a5: float
    :param a6: float
    :param a7: float
    :param a8: float
    :param a9: float
    :param a10: float
    :param a11: float
    :return:
    """
    x, y, t = xdata
    return (a1 * x ** 2) + (a2 * x) + (a3 * y ** 2) + (a4 * y) + (a5 * t ** 2) + (a6 * t) + (a7 * x * y) + (
          a8 * x * t) + (a9 * y * t) + (a10 * x * y * t) + a11
