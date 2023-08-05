"""
EnergySystem module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
Code contributors: Peter Yefi peteryefi@gmail.com
"""

from hub.city_model_structure.city_object import CityObject
from hub.city_model_structure.energy_systems.air_source_hp import AirSourceHP
from hub.city_model_structure.energy_systems.water_to_water_hp import WaterToWaterHP


class EnergySystem(CityObject):
  """
  EnergySystem(CityObject) class
  """

  def __init__(self, name, surfaces):
    super().__init__(name, surfaces)
    self._air_source_hp = None
    self._water_to_water_hp = None
    self._type = 'energy_system'

  @property
  def air_source_hp(self) -> AirSourceHP:
    """
    Heat pump energy system
    :return:
    """
    return self._air_source_hp

  @air_source_hp.setter
  def air_source_hp(self, value):
    """
    Set heat pump for energy system
    :param value: AirSourceHP
    """
    if self._air_source_hp is None:
      self._air_source_hp = value

  @property
  def water_to_water_hp(self) -> WaterToWaterHP:
    """
    Water to water heat pump energy system
    :return:
    """
    return self._water_to_water_hp

  @water_to_water_hp.setter
  def water_to_water_hp(self, value):
    """
    Set water to water heat pump for energy system
    :param value: WaterToWaterHP
    """
    if self._water_to_water_hp is None:
      self._water_to_water_hp = value

  @property
  def type(self) -> str:
    """
    Type of city object
    :return: str
    """
    return self._type
