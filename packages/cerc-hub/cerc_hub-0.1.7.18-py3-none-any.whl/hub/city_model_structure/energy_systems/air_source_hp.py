"""
air_source_hp module defines an air source heat pump
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
Code contributors: Peter Yefi peteryefi@gmail.com
"""

from typing import List
from hub.city_model_structure.energy_systems.heat_pump import HeatPump


class AirSourceHP(HeatPump):
  """
  AirSourceHP class
  """

  def __init__(self):
    super().__init__()
    self._cooling_capacity = None
    self._cooling_comp_power = None
    self._cooling_capacity_coff = None  # a coefficients for insel
    self._heating_capacity = None
    self._heating_comp_power = None
    self._heating_capacity_coff = None

  @property
  def cooling_capacity(self) -> List[float]:
    """
    Get cooling capacity in kW
    :return: [[float]]
    """
    return self._cooling_capacity

  @cooling_capacity.setter
  def cooling_capacity(self, value):
    """
    Set cooling capacity in kW
    :param value: [[float]]
    """
    if self._cooling_capacity is None:
      self._cooling_capacity = value

  @property
  def cooling_comp_power(self) -> List[float]:
    """
    Get cooling compressor power input in kW
    :return: [[float]]
    """
    return self._cooling_comp_power

  @cooling_comp_power.setter
  def cooling_comp_power(self, value):
    """
    Set the cooling compressor in kW
    :param value: [[float]]
    :return:
    """
    if self._cooling_comp_power is None:
      self._cooling_comp_power = value

  @property
  def cooling_capacity_coff(self) -> List[float]:
    """
    Get cooling capacity coefficients
    :return: [float]
    """
    return self._cooling_capacity_coff

  @cooling_capacity_coff.setter
  def cooling_capacity_coff(self, value):
    """
    Set the value for cooling capacity coefficients
    :param value: [float]
    :return:
    """
    if self._cooling_capacity_coff is None:
      self._cooling_capacity_coff = value

  @property
  def heating_capacity(self) -> List[float]:
    """
    Get heating capacity kW
    :return: [[float]]
    """
    return self._heating_capacity

  @heating_capacity.setter
  def heating_capacity(self, value):
    """
    Set the heating capacity in kW
    :param value: [[float]]
    :return:
    """
    if self._heating_capacity is None:
      self._heating_capacity = value

  @property
  def heating_comp_power(self) -> List[float]:
    """
    Get heating compressor power kW
    :return: [[float]]
    """
    return self._heating_comp_power

  @heating_comp_power.setter
  def heating_comp_power(self, value):
    """
    Set the heating compressor power in kW
    :param value: [[float]]
    :return:
    """
    if self._heating_comp_power is None:
      self._heating_comp_power = value

  @property
  def heating_capacity_coff(self) -> List[float]:
    """
    Get heating capacity coefficients
    :return: [float]
    """
    return self._heating_capacity_coff

  @heating_capacity_coff.setter
  def heating_capacity_coff(self, value):
    """
    Set the value for heating capacity coefficients
    :param value: [float]
    :return:
    """
    if self._heating_capacity_coff is None:
      self._heating_capacity_coff = value
