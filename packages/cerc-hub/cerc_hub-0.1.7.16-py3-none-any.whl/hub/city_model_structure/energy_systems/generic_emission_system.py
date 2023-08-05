"""
Generic energy emission system module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""


class GenericEmissionSystem:
  """
  GenericEmissionSystem class
  """
  def __init__(self):
    self._parasitic_energy_consumption = None

  @property
  def parasitic_energy_consumption(self):
    """
    Get parasitic_energy_consumption in ratio (W/W)
    :return: float
    """
    return self._parasitic_energy_consumption

  @parasitic_energy_consumption.setter
  def parasitic_energy_consumption(self, value):
    """
    Set parasitic_energy_consumption in ratio (W/W)
    :param value: float
    """
    self._parasitic_energy_consumption = value
