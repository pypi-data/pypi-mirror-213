"""
InternalZone module. It saves the original geometrical information from interiors together with some attributes of those
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

import uuid
from typing import Union, List
from hub.city_model_structure.building_demand.usage import Usage
from hub.city_model_structure.building_demand.thermal_zone import ThermalZone
from hub.city_model_structure.attributes.polyhedron import Polyhedron
from hub.city_model_structure.energy_systems.hvac_system import HvacSystem


class InternalZone:
  """
  InternalZone class
  """
  def __init__(self, surfaces, area):
    self._surfaces = surfaces
    self._id = None
    self._geometry = None
    self._volume = None
    self._area = area
    self._thermal_zones = None
    self._usages = None
    self._hvac_system = None

  @property
  def id(self):
    """
    Get internal zone id, a universally unique identifier randomly generated
    :return: str
    """
    if self._id is None:
      self._id = uuid.uuid4()
    return self._id

  @property
  def geometry(self) -> Polyhedron:
    """
    Get internal zone geometry
    :return: Polyhedron
    """
    if self._geometry is None:
      polygons = []
      for surface in self.surfaces:
        polygons.append(surface.perimeter_polygon)
      self._geometry = Polyhedron(polygons)
    return self._geometry

  @property
  def surfaces(self):
    """
    Get internal zone surfaces
    :return: [Surface]
    """
    return self._surfaces

  @property
  def volume(self):
    """
    Get internal zone volume in cubic meters
    :return: float
    """
    return self.geometry.volume

  @property
  def area(self):
    """
    Get internal zone area in square meters
    :return: float
    """
    return self._area

  @property
  def usages(self) -> [Usage]:
    """
    Get internal zone usage zones
    :return: [Usage]
    """
    return self._usages

  @usages.setter
  def usages(self, value):
    """
    Set internal zone usage zones
    :param value: [Usage]
    """
    self._usages = value

  @property
  def hvac_system(self) -> Union[None, HvacSystem]:
    """
    Get HVAC system installed for this thermal zone
    :return: None or HvacSystem
    """
    return self._hvac_system

  @hvac_system.setter
  def hvac_system(self, value):
    """
    Set HVAC system installed for this thermal zone
    :param value: HvacSystem
    """
    self._hvac_system = value

  @property
  def thermal_zones(self) -> Union[None, List[ThermalZone]]:
    """
    Get building thermal zones
    :return: [ThermalZone]
    """
    return self._thermal_zones

  @thermal_zones.setter
  def thermal_zones(self, value):
    """
    Set city object thermal zones
    :param value: [ThermalZone]
    """
    self._thermal_zones = value
