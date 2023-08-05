"""
Simplified Radiosity Algorithm
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guillermo.GutierrezMorote@concordia.ca
"""
import calendar as cal
import pandas as pd
import numpy as np
import hub.helpers.constants as cte


class SimplifiedRadiosityAlgorithm:
  """
  Import SRA results
  """
  def __init__(self, city, base_path):

    self._city = city
    self._base_path = base_path
    self._input_file_path = (self._base_path / f'{self._city.name}_sra_SW.out').resolve()
    self._month_hour = self._month_hour_data_frame
    self._results = self._read_results()
    self._radiation_list = []

  @property
  def _month_hour_data_frame(self):
    array = []
    for i in range(0, 12):
      days_of_month = cal.monthrange(2015, i+1)[1]
      total_hours = days_of_month * 24
      array = np.concatenate((array, np.full(total_hours, i + 1)))
    return pd.DataFrame(array, columns=[cte.MONTH])

  def _get_monthly_values(self, values):
    out = None
    if values is not None:
      if cte.MONTH not in values.columns:
        values = pd.concat([self._month_hour, pd.DataFrame(values)], axis=1)
      out = values.groupby(cte.MONTH, as_index=False).sum()
      del out[cte.MONTH]
    return out

  @staticmethod
  def _get_yearly_values(values):
    return [values.sum()]

  def _read_results(self):
    try:
      return pd.read_csv(self._input_file_path, sep='\s+', header=0)
    except FileNotFoundError as err:
      raise FileNotFoundError('No SRA output file found') from err

  @property
  def _radiation(self) -> []:
    if len(self._radiation_list) == 0:
      id_building = ''
      header_building = []
      for column in self._results.columns.values:
        if id_building != column.split(':')[1]:
          id_building = column.split(':')[1]
          if len(header_building) > 0:
            self._radiation_list.append(pd.concat([self._month_hour, self._results[header_building]], axis=1))
          header_building = [column]
        else:
          header_building.append(column)
      self._radiation_list.append(pd.concat([self._month_hour, self._results[header_building]], axis=1))
    return self._radiation_list

  def enrich(self):
    """
    saves in building surfaces the correspondent irradiance at different time-scales depending on the mode
    if building is None, it saves all buildings' surfaces in file, if building is specified, it saves only that
    specific building values
    :return: none
    """
    for radiation in self._radiation:
      city_object_name = radiation.columns.values.tolist()[1].split(':')[1]
      building = self._city.city_object(city_object_name)
      for column in radiation.columns.values:
        if column == cte.MONTH:
          continue
        header_id = column
        surface_id = header_id.split(':')[2]
        surface = building.surface_by_id(surface_id)
        new_value = pd.DataFrame(radiation[[header_id]].to_numpy(), columns=[cte.SRA])
        month_new_value = self._get_monthly_values(new_value)
        if cte.MONTH not in surface.global_irradiance:
          surface.global_irradiance[cte.MONTH] = month_new_value
        else:
          pd.concat([surface.global_irradiance[cte.MONTH], month_new_value], axis=1)
        if cte.HOUR not in surface.global_irradiance:
          surface.global_irradiance[cte.HOUR] = new_value
        else:
          pd.concat([surface.global_irradiance[cte.HOUR], new_value], axis=1)
        if cte.YEAR not in surface.global_irradiance:
          surface.global_irradiance[cte.YEAR] = pd.DataFrame(SimplifiedRadiosityAlgorithm._get_yearly_values(new_value),
                                                             columns=[cte.SRA])
    self._city.level_of_detail.surface_radiation = 2
    for building in self._city.buildings:
      building.level_of_detail.surface_radiation = 2
