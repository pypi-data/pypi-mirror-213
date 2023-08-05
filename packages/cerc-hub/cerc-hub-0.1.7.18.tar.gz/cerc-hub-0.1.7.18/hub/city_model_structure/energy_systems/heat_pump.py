"""
heat_pump module defines a heat pump
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""
from typing import List
from pandas.core.series import Series


class HeatPump:
  """
  HeatPump class
  """

  def __init__(self):
    self._model = None
    self._hp_monthly_fossil_consumption = None
    self._hp_monthly_electricity_demand = None

  @property
  def model(self) -> str:
    """
    Get model name
    :return: str
    """
    return self._model

  @model.setter
  def model(self, value):
    """
    Set model (name, indicated in capacity)
    :param value: str
    """
    if self._model is None:
      self._model = value

  @property
  def hp_monthly_fossil_consumption(self) -> List:
    """
    Fossil fuel consumption that results from insel simulation
    ":return: []
    :return:
    """
    return self._hp_monthly_fossil_consumption

  @hp_monthly_fossil_consumption.setter
  def hp_monthly_fossil_consumption(self, value):
    if isinstance(value, Series):
      self._hp_monthly_fossil_consumption = value

  @property
  def hp_monthly_electricity_demand(self) -> List:
    """
    Electricity demand that results from insel simulation
    ":return: []
    :return:
    """
    return self._hp_monthly_electricity_demand

  @hp_monthly_electricity_demand.setter
  def hp_monthly_electricity_demand(self, value):
    if isinstance(value, Series):
      self._hp_monthly_electricity_demand = value
