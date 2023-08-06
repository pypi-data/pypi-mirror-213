"""
EpwWeatherParameters class to extract weather parameters from a defined region in .epw format (EnergyPlus Weather)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
import logging
import sys
from pathlib import Path

import pandas as pd
import requests

import hub.helpers.constants as cte
from hub.city_model_structure.city import City
from hub.imports.weather.helpers.weather import Weather as wh


class EpwWeatherParameters:
  """
  EpwWeatherParameters class
  """
  def __init__(self, city: City):
    self._weather_values = None
    self._city = city
    self._url = wh().epw_file(city.region_code)
    self._path = (Path(__file__).parent.parent.parent / f'data/weather/epw/{self._url.rsplit("/", 1)[1]}').resolve()
    if not self._path.exists():
      with open(self._path, 'wb') as epw_file:
        epw_file.write(requests.get(self._url, allow_redirects=True).content)

    try:
      with open(self._path, 'r', encoding='utf8') as file:
        line = file.readline().split(',')
        city.climate_reference_city = line[1]
        city.latitude = line[6]
        city.longitude = line[7]
        city.time_zone = line[8]
        for i in range(0, 2):
          _ = file.readline().split(',')
        line = file.readline().split(',')
        number_records = int(line[1])
        ground_temperature = {}
        for i in range(0, number_records):
          depth_measurement_ground_temperature = line[i*16+2]
          temperatures = []
          for j in range(0, 12):
            temperatures.append(float(line[i*16+j+6]))
          ground_temperature[depth_measurement_ground_temperature] = temperatures
    except SystemExit:
      logging.error('Error: weather file %s not found. Please download it from https://energyplus.net/weather and place'
                    ' it in folder data\\weather\\epw', self._path)
      sys.exit()

    try:
      self._weather_values = pd.read_csv(self._path, header=0, skiprows=7,
                                         names=['year', 'month', 'day', 'hour', 'minute',
                                                'data_source_and_uncertainty_flags',
                                                'dry_bulb_temperature_c', 'dew_point_temperature_c',
                                                'relative_humidity_perc',
                                                'atmospheric_station_pressure_pa',
                                                'extraterrestrial_horizontal_radiation_wh_m2',
                                                'extraterrestrial_direct_normal_radiation_wh_m2',
                                                'horizontal_infrared_radiation_intensity_wh_m2',
                                                'global_horizontal_radiation_wh_m2', 'direct_normal_radiation_wh_m2',
                                                'diffuse_horizontal_radiation_wh_m2',
                                                'global_horizontal_illuminance_lux',
                                                'direct_normal_illuminance_lux', 'diffuse_horizontal_illuminance_lux',
                                                'zenith_luminance_cd_m2',
                                                'wind_direction_deg', 'wind_speed_m_s', 'total_sky_cover',
                                                'opaque_sky_cover', 'visibility_km',
                                                'ceiling_heigh_m_s', 'present_weather_observation',
                                                'present_weather_codes',
                                                'precipitable_water_mm', 'aerosol_optical_depth_10_3_ths',
                                                'snow_depth_cm',
                                                'days_since_last_snowfall', 'albedo', 'liquid_precipitation_depth_mm',
                                                'liquid_precipitation_quality_hr'])
    except SystemExit:
      sys.stderr.write(f'Error: wrong formatting of weather file {self._path}\n')
      sys.exit()
    for building in self._city.buildings:
      building.ground_temperature[cte.MONTH] = ground_temperature
      ground_temperature = {}
      for ground_temperature_set in building.ground_temperature[cte.MONTH]:
        temperature = 0
        for value in building.ground_temperature[cte.MONTH][ground_temperature_set]:
          temperature += value / 12
        ground_temperature[ground_temperature_set] = [temperature]
      building.ground_temperature[cte.YEAR] = ground_temperature
      if cte.HOUR in building.external_temperature:
        del building.external_temperature[cte.HOUR]
      new_value = pd.DataFrame(self._weather_values[['dry_bulb_temperature_c']].to_numpy(), columns=['epw'])
      number_invalid_records = new_value[new_value.epw == 99.9].count().epw
      if number_invalid_records > 0:
        sys.stderr.write(f'Warning: {self._path} invalid records (value of 99.9) in dry bulb temperature\n')
      if cte.HOUR not in building.external_temperature:
        building.external_temperature[cte.HOUR] = new_value
      else:
        pd.concat([building.external_temperature[cte.HOUR], new_value], axis=1)

      new_value = pd.DataFrame(self._weather_values[['global_horizontal_radiation_wh_m2']].to_numpy(), columns=['epw'])
      number_invalid_records = new_value[new_value.epw == 9999].count().epw
      if number_invalid_records > 0:
        sys.stderr.write(f'Warning: {self._path} invalid records (value of 9999) in global horizontal radiation\n')
      if cte.HOUR not in building.global_horizontal:
        building.global_horizontal[cte.HOUR] = new_value
      else:
        pd.concat([building.global_horizontal[cte.HOUR], new_value], axis=1)

      new_value = pd.DataFrame(self._weather_values[['diffuse_horizontal_radiation_wh_m2']].to_numpy(), columns=['epw'])
      number_invalid_records = new_value[new_value.epw == 9999].count().epw
      if number_invalid_records > 0:
        sys.stderr.write(f'Warning: {self._path} invalid records (value of 9999) in diffuse horizontal radiation\n')
      if cte.HOUR not in building.diffuse:
        building.diffuse[cte.HOUR] = new_value
      else:
        pd.concat([building.diffuse[cte.HOUR], new_value], axis=1)

      new_value = pd.DataFrame(self._weather_values[['direct_normal_radiation_wh_m2']].to_numpy(), columns=['epw'])
      number_invalid_records = new_value[new_value.epw == 9999].count().epw
      if number_invalid_records > 0:
        sys.stderr.write(f'Warning: {self._path} invalid records (value of 9999) in direct horizontal radiation\n')
      if cte.HOUR not in building.beam:
        building.beam[cte.HOUR] = new_value
      else:
        pd.concat([building.beam[cte.HOUR], new_value], axis=1)

      new_value = wh().cold_water_temperature(building.external_temperature[cte.HOUR]['epw'])
      if cte.HOUR not in building.cold_water_temperature:
        building.cold_water_temperature[cte.HOUR] = new_value
      else:
        pd.concat([building.cold_water_temperature[cte.HOUR], new_value], axis=1)
    # create the monthly and yearly values out of the hourly
    for building in self._city.buildings:
      if cte.MONTH not in building.external_temperature:
        building.external_temperature[cte.MONTH] = \
          wh().get_monthly_mean_values(building.external_temperature[cte.HOUR][['epw']])
      if cte.YEAR not in building.external_temperature:
        building.external_temperature[cte.YEAR] = \
          wh(). get_yearly_mean_values(building.external_temperature[cte.HOUR][['epw']])
      if cte.MONTH not in building.cold_water_temperature:
        building.cold_water_temperature[cte.MONTH] = wh().get_monthly_mean_values(
          building.cold_water_temperature[cte.HOUR][['epw']])
      if cte.YEAR not in building.cold_water_temperature:
        building.cold_water_temperature[cte.YEAR] = wh().get_yearly_mean_values(
          building.cold_water_temperature[cte.HOUR][['epw']])

      # If the usage has already being imported, the domestic hot water missing values must be calculated here that
      # the cold water temperature is finally known
      cold_temperature = building.cold_water_temperature[cte.YEAR]['epw']
      for internal_zone in building.internal_zones:
        if internal_zone.usages is not None:
          for usage in internal_zone.usages:
            if usage.domestic_hot_water.peak_flow is None:
              if usage.domestic_hot_water.density is None:
                continue
              peak_flow = 0
              if (usage.domestic_hot_water.service_temperature - cold_temperature) > 0:
                peak_flow = usage.domestic_hot_water.density / cte.WATER_DENSITY / cte.WATER_HEAT_CAPACITY \
                      / (usage.domestic_hot_water.service_temperature - cold_temperature)
              usage.domestic_hot_water.peak_flow = peak_flow
            if usage.domestic_hot_water.density is None:
              if usage.domestic_hot_water.peak_flow is None:
                continue
              density = (
                  usage.domestic_hot_water.peak_flow * cte.WATER_DENSITY * cte.WATER_HEAT_CAPACITY *
                  (usage.domestic_hot_water.service_temperature - cold_temperature)
              )
              usage.domestic_hot_water.density = density

    self._city.level_of_detail.weather = 2
    for building in self._city.buildings:
      building.level_of_detail.weather = 2
