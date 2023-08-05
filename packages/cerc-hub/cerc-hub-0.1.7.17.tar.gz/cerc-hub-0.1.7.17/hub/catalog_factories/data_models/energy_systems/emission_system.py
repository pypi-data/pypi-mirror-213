"""
Energy System catalog emission system
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""


class EmissionSystem:
  """
  Emission system class
  """
  def __init__(self, system_id, name, system_type, parasitic_energy_consumption):

    self._system_id = system_id
    self._name = name
    self._type = system_type
    self._parasitic_energy_consumption = parasitic_energy_consumption

  @property
  def id(self):
    """
    Get system id
    :return: float
    """
    return self._system_id

  @id.setter
  def id(self, value):
    """
    Set system id
    :param value: float
    """
    self._system_id = value

  @property
  def name(self):
    """
    Get name
    :return: string
    """
    return self._name

  @name.setter
  def name(self, value):
    """
    Set name
    :param value: string
    """
    self._name = value

  @property
  def type(self):
    """
    Get type
    :return: string
    """
    return self._type

  @property
  def parasitic_energy_consumption(self):
    """
    Get parasitic_energy_consumption in ratio (Wh/Wh)
    :return: float
    """
    return self._parasitic_energy_consumption
