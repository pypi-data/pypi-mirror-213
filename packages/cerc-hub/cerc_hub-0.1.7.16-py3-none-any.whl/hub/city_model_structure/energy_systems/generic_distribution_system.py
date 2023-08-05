"""
Generic energy distribution system definition
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""


class GenericDistributionSystem:
  """
  GenericDistributionSystem class
  """
  def __init__(self):
    self._type = None
    self._supply_temperature = None
    self._distribution_consumption_fix_flow = None
    self._distribution_consumption_variable_flow = None
    self._heat_losses = None

  @property
  def type(self):
    """
    Get type from [air, water, refrigerant]
    :return: string
    """
    return self._type

  @type.setter
  def type(self, value):
    """
    Set type from [air, water, refrigerant]
    :param value: string
    """
    self._type = value

  @property
  def supply_temperature(self):
    """
    Get supply_temperature in degree Celsius
    :return: float
    """
    return self._supply_temperature

  @supply_temperature.setter
  def supply_temperature(self, value):
    """
    Set supply_temperature in degree Celsius
    :param value: float
    """
    self._supply_temperature = value

  @property
  def distribution_consumption_fix_flow(self):
    """
    Get distribution_consumption if the pump or fan work at fix mass or volume flow in ratio over peak power (W/W)
    :return: float
    """
    return self._distribution_consumption_fix_flow

  @distribution_consumption_fix_flow.setter
  def distribution_consumption_fix_flow(self, value):
    """
    Set distribution_consumption if the pump or fan work at fix mass or volume flow in ratio over peak power (W/W)
    :return: float
    """
    self._distribution_consumption_fix_flow = value

  @property
  def distribution_consumption_variable_flow(self):
    """
    Get distribution_consumption if the pump or fan work at variable mass or volume flow in ratio
    over energy produced (Wh/Wh)
    :return: float
    """
    return self._distribution_consumption_variable_flow

  @distribution_consumption_variable_flow.setter
  def distribution_consumption_variable_flow(self, value):
    """
    Set distribution_consumption if the pump or fan work at variable mass or volume flow in ratio
    over energy produced (Wh/Wh)
    :return: float
    """
    self._distribution_consumption_variable_flow = value

  @property
  def heat_losses(self):
    """
    Get heat_losses in ratio over energy produced
    :return: float
    """
    return self._heat_losses

  @heat_losses.setter
  def heat_losses(self, value):
    """
    Set heat_losses in ratio over energy produced
    :param value: float
    """
    self._heat_losses = value
