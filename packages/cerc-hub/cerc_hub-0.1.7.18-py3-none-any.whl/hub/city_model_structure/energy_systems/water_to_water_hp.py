"""
water_to_water_hp module defines a water to water heat pump heat pump
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""

from typing import List
from hub.city_model_structure.energy_systems.heat_pump import HeatPump


class WaterToWaterHP(HeatPump):
  """
  WaterToWaterHP class
  """

  def __init__(self):
    super().__init__()
    self._entering_water_temp = None
    self._leaving_water_temp = None
    self._total_cooling_capacity = None
    self._power_demand = None
    self._flow_rate = None
    self._power_demand_coff = None  # a coefficients

  @property
  def entering_water_temp(self) -> List[float]:
    """
    Get entering water temperature in degree celsius
    :return: [[float]]
    """
    return self._entering_water_temp

  @entering_water_temp.setter
  def entering_water_temp(self, value):
    """
    Set entering water temperature in degree celsius
    :param value: [[float]]
    """
    if self._entering_water_temp is None:
      self._entering_water_temp = value

  @property
  def leaving_water_temp(self) -> List[float]:
    """
    Get leaving water temperature in degree celsius
    :return: [[float]]
    """
    return self._leaving_water_temp

  @leaving_water_temp.setter
  def leaving_water_temp(self, value):
    """
    Set the leaving water temperature in degree celsius
    :param value: [[float]]
    :return:
    """
    if self._leaving_water_temp is None:
      self._leaving_water_temp = value

  @property
  def total_cooling_capacity(self) -> List[float]:
    """
    Get total cooling capacity
    :return: [float]
    """
    return self._total_cooling_capacity

  @total_cooling_capacity.setter
  def total_cooling_capacity(self, value):
    """
    Set the value for total cooling capacity
    :param value: [float]
    :return:
    """
    if self._total_cooling_capacity is None:
      self._total_cooling_capacity = value

  @property
  def power_demand(self) -> List[float]:
    """
    Get power demand in kW
    :return: [float]
    """
    return self._power_demand

  @power_demand.setter
  def power_demand(self, value):
    """
    Set the value for power demand in kW
    :param value: [float]
    :return:
    """
    if self._power_demand is None:
      self._power_demand = value

  @property
  def flow_rate(self) -> List[float]:
    """
    Get flow rate in kg/s
    :return: [[float]]
    """
    return self._flow_rate

  @flow_rate.setter
  def flow_rate(self, value):
    """
    Set flow rate in kW
    :param value: [[float]]
    :return:
    """
    if self._flow_rate is None:
      self._flow_rate = value

  @property
  def power_demand_coff(self) -> List[float]:
    """
    Get power demand coefficients
    :return: [float]
    """
    return self._power_demand_coff

  @power_demand_coff.setter
  def power_demand_coff(self, value):
    """
    Set the value for power demand coefficients
    :param value: [float]
    :return:
    """
    if self._power_demand_coff is None:
      self._power_demand_coff = value
