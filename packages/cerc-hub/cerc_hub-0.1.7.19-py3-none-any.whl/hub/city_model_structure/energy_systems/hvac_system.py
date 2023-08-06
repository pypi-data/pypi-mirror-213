"""
HvacSystem module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
from typing import Union, List
from hub.city_model_structure.building_demand.thermal_zone import ThermalZone


class HvacSystem:
  """
  HvacSystem class
  """
  def __init__(self):
    self._type = None
    self._thermal_zones = None

  @property
  def type(self) -> Union[None, str]:
    """
    Get hvac system type
    :return: None or str
    """
    return self._type

  @type.setter
  def type(self, value):
    """
    Set hvac system type
    :param value: str
    """
    if value is not None:
      self._type = str(value)

  @property
  def thermal_zones(self) -> Union[None, List[ThermalZone]]:
    """
    Get list of zones that this unit serves
    :return: None or [ThermalZone]
    """
    return self._thermal_zones

  @thermal_zones.setter
  def thermal_zones(self, value):
    """
    Set list of zones that this unit serves
    :param value: [ThermalZone]
    """
    self._thermal_zones = value
