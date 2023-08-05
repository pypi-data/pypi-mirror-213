"""
Monthly values module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2020 Project Author Pilar Monsalvete pilar_monsalvete@yahoo.es
"""
import calendar as cal
import pandas as pd
import numpy as np


class MonthlyValues:
  """
  Monthly values class
  """
  def __init__(self):
    self._month_hour = None

  def get_mean_values(self, values):
    """
    Calculates the mean values for each month
    :return: DataFrame(float)
    """
    out = None
    if values is not None:
      if 'month' not in values.columns:
        values = pd.concat([self.month_hour, pd.DataFrame(values)], axis=1)
      out = values.groupby('month', as_index=False).mean()
      del out['month']
    return out

  def get_total_month(self, values):
    """
    Calculates the total value for each month
    :return: DataFrame(int)
    """
    out = None
    if values is not None:
      if 'month' not in values.columns:
        values = pd.concat([self.month_hour, pd.DataFrame(values)], axis=1)
      out = pd.DataFrame(values).groupby('month', as_index=False).sum()
      del out['month']
    return out

  @property
  def month_hour(self):
    """
    returns a DataFrame that has x values of the month number (January = 1, February = 2...),
    being x the number of hours of the corresponding month
    :return: DataFrame(int)
    """
    array = []
    for i in range(0, 12):
      days_of_month = cal.monthrange(2015, i+1)[1]
      total_hours = days_of_month * 24
      array = np.concatenate((array, np.full(total_hours, i + 1)))
    self._month_hour = pd.DataFrame(array, columns=['month'])
    return self._month_hour
