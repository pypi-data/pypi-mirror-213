"""
Insel monthly energy balance
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guillermo.GutierrezMorote@concordia.ca
"""
from pathlib import Path
import csv
import pandas as pd

import hub.helpers.constants as cte


class InselMonthlyEnergyBalance:
  """
  Import insel monthly energy balance results
  """
  def __init__(self, city, base_path):

    self._city = city
    self._base_path = base_path

  @staticmethod
  def _conditioning_demand(insel_output_file_path):
    heating = []
    cooling = []
    with open(Path(insel_output_file_path).resolve(), 'r', encoding='utf8') as csv_file:
      csv_reader = csv.reader(csv_file)
      for line in csv_reader:
        demand = str(line).replace("['", '').replace("']", '').split()
        for i in range(0, 2):
          if demand[i] != 'NaN':
            aux = float(demand[i]) * 1000  # kWh to Wh
            demand[i] = str(aux)
          else:
            demand[i] = '0'
        heating.append(demand[0])
        cooling.append(demand[1])
    monthly_heating = pd.DataFrame(heating, columns=[cte.INSEL_MEB]).astype(float)
    monthly_cooling = pd.DataFrame(cooling, columns=[cte.INSEL_MEB]).astype(float)
    return monthly_heating, monthly_cooling

  def _dhw_and_electric_demand(self):
    for building in self._city.buildings:
      domestic_hot_water_demand = []
      lighting_demand = []
      appliances_demand = []
      if building.internal_zones[0].thermal_zones is None:
        domestic_hot_water_demand = [0] * 12
        lighting_demand = [0] * 12
        appliances_demand = [0] * 12
      else:
        thermal_zone = building.internal_zones[0].thermal_zones[0]
        area = thermal_zone.total_floor_area
        cold_water = building.cold_water_temperature[cte.MONTH]['epw']
        peak_flow = thermal_zone.domestic_hot_water.peak_flow
        service_temperature = thermal_zone.domestic_hot_water.service_temperature
        lighting_density = thermal_zone.lighting.density
        appliances_density = thermal_zone.appliances.density

        for month in range(0, 12):
          total_dhw_demand = 0
          total_lighting = 0
          total_appliances = 0

          for schedule in thermal_zone.lighting.schedules:
            total_day = 0
            for value in schedule.values:
              total_day += value
            for day_type in schedule.day_types:
              total_lighting += total_day * cte.DAYS_A_MONTH[day_type][month] * lighting_density
          lighting_demand.append(total_lighting * area)

          for schedule in thermal_zone.appliances.schedules:
            total_day = 0
            for value in schedule.values:
              total_day += value
            for day_type in schedule.day_types:
              total_appliances += total_day * cte.DAYS_A_MONTH[day_type][month] * appliances_density
          appliances_demand.append(total_appliances * area)

          for schedule in thermal_zone.domestic_hot_water.schedules:
            total_day = 0
            for value in schedule.values:
              total_day += value
            for day_type in schedule.day_types:
              demand = (
                  peak_flow * cte.WATER_DENSITY * cte.WATER_HEAT_CAPACITY * (service_temperature - cold_water[month])
              )
              total_dhw_demand += total_day * cte.DAYS_A_MONTH[day_type][month] * demand
          domestic_hot_water_demand.append(total_dhw_demand * area)

      building.domestic_hot_water_heat_demand[cte.MONTH] = pd.DataFrame(domestic_hot_water_demand,
                                                                        columns=[cte.INSEL_MEB])
      yearly_domestic_hot_water_demand = [sum(domestic_hot_water_demand)]
      building.domestic_hot_water_heat_demand[cte.YEAR] = pd.DataFrame(yearly_domestic_hot_water_demand,
                                                                       columns=[cte.INSEL_MEB])
      building.lighting_electrical_demand[cte.MONTH] = pd.DataFrame(lighting_demand, columns=[cte.INSEL_MEB])
      yearly_lighting_electrical_demand = [sum(lighting_demand)]
      building.lighting_electrical_demand[cte.YEAR] = pd.DataFrame(
        yearly_lighting_electrical_demand,
        columns=[cte.INSEL_MEB]
      )
      building.appliances_electrical_demand[cte.MONTH] = pd.DataFrame(appliances_demand, columns=[cte.INSEL_MEB])
      yearly_appliances_electrical_demand = [sum(appliances_demand)]
      building.appliances_electrical_demand[cte.YEAR] = pd.DataFrame(
        yearly_appliances_electrical_demand,
        columns=[cte.INSEL_MEB]
      )

  def enrich(self):
    """
    Enrich the city by using the insel monthly energy balance output files
    :return: None
    """
    for building in self._city.buildings:
      file_name = building.name + '.out'
      insel_output_file_path = Path(self._base_path / file_name).resolve()
      if insel_output_file_path.is_file():
        building.heating_demand[cte.MONTH], building.cooling_demand[cte.MONTH] = self._conditioning_demand(insel_output_file_path)
        building.heating_demand[cte.YEAR] = pd.DataFrame(
          [building.heating_demand[cte.MONTH][cte.INSEL_MEB].astype(float).sum()], columns=[cte.INSEL_MEB]
        )
        building.cooling_demand[cte.YEAR] = pd.DataFrame(
          [building.cooling_demand[cte.MONTH][cte.INSEL_MEB].astype(float).sum()], columns=[cte.INSEL_MEB]
        )
    self._dhw_and_electric_demand()
