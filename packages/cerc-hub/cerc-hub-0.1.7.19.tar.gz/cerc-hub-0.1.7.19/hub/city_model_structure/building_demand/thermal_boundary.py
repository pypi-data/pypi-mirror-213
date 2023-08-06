"""
ThermalBoundary module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributors: Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

import uuid
from typing import List, Union, TypeVar
from hub.helpers.configuration_helper import ConfigurationHelper as ch
import hub.helpers.constants as cte
from hub.city_model_structure.building_demand.layer import Layer
from hub.city_model_structure.building_demand.thermal_opening import ThermalOpening
from hub.city_model_structure.building_demand.thermal_zone import ThermalZone

Surface = TypeVar('Surface')


class ThermalBoundary:
  """
  ThermalBoundary class
  """
  def __init__(self, parent_surface, opaque_area, windows_areas):
    self._parent_surface = parent_surface
    self._opaque_area = opaque_area
    self._windows_areas = windows_areas
    self._id = None
    self._thermal_zones = None
    self._thermal_openings = None
    self._layers = None
    self._he = ch().convective_heat_transfer_coefficient_exterior
    self._hi = ch().convective_heat_transfer_coefficient_interior
    self._u_value = None
    self._construction_name = None
    self._thickness = None
    self._internal_surface = None
    self._window_ratio = None
    self._window_ratio_is_calculated = False

  @property
  def id(self):
    """
    Get thermal zone id, a universally unique identifier randomly generated
    :return: str
    """
    if self._id is None:
      self._id = uuid.uuid4()
    return self._id

  @property
  def parent_surface(self) -> Surface:
    """
    Get the surface that belongs to the thermal boundary
    :return: Surface
    """
    return self._parent_surface

  @property
  def thermal_zones(self) -> List[ThermalZone]:
    """
    Get the thermal zones delimited by the thermal boundary
    :return: [ThermalZone]
    """
    return self._thermal_zones

  @thermal_zones.setter
  def thermal_zones(self, value):
    """
    Get the thermal zones delimited by the thermal boundary
    :param value: [ThermalZone]
    """
    self._thermal_zones = value

  @property
  def opaque_area(self):
    """
    Get the thermal boundary area in square meters
    :return: float
    """
    return float(self._opaque_area)

  @property
  def thickness(self):
    """
    Get the thermal boundary thickness in meters
    :return: float
    """
    if self._thickness is None:
      self._thickness = 0.0
      if self.layers is not None:
        for layer in self.layers:
          if not layer.material.no_mass:
            self._thickness += layer.thickness
    return self._thickness

  @property
  def thermal_openings(self) -> Union[None, List[ThermalOpening]]:
    """
    Get thermal boundary thermal openings
    :return: None or [ThermalOpening]
    """
    if self._thermal_openings is None:
      if self.window_ratio is not None:
        if self.window_ratio == 0:
          self._thermal_openings = []
        else:
          thermal_opening = ThermalOpening()
          if self.window_ratio == 1:
            _area = self.opaque_area
          else:
            _area = self.opaque_area * self.window_ratio / (1-self.window_ratio)
          thermal_opening.area = _area
          self._thermal_openings = [thermal_opening]
      else:
        if len(self.windows_areas) > 0:
          self._thermal_openings = []
          for window_area in self.windows_areas:
            thermal_opening = ThermalOpening()
            thermal_opening.area = window_area
            self._thermal_openings.append(thermal_opening)
        else:
          self._thermal_openings = []
    return self._thermal_openings

  @property
  def construction_name(self) -> Union[None, str]:
    """
    Get construction name
    :return: None or str
    """
    return self._construction_name

  @construction_name.setter
  def construction_name(self, value):
    """
    Set construction name
    :param value: str
    """
    if value is not None:
      self._construction_name = str(value)

  @property
  def layers(self) -> List[Layer]:
    """
    Get thermal boundary layers
    :return: [Layers]
    """
    return self._layers

  @layers.setter
  def layers(self, value):
    """
    Set thermal boundary layers
    :param value: [Layer]
    """
    self._layers = value

  @property
  def type(self):
    """
    Get thermal boundary surface type
    :return: str
    """
    return self.parent_surface.type

  @property
  def window_ratio(self) -> Union[None, float]:
    """
    Get thermal boundary window ratio
    It returns the window ratio calculated as the total windows' areas in a wall divided by
    the total (opaque + transparent) area of that wall if windows are defined in the geometry imported.
    If not, it returns the window ratio imported from an external source (e.g. construction library, manually assigned).
    If none of those sources are available, it returns None.
    :return: float
    """
    if self.windows_areas is not None:
      if not self._window_ratio_is_calculated:
        _calculated = True
        if len(self.windows_areas) == 0:
          self._window_ratio = 0
        else:
          total_window_area = 0
          for window_area in self.windows_areas:
            total_window_area += window_area
          self._window_ratio = total_window_area / (self.opaque_area + total_window_area)
    return self._window_ratio

  @window_ratio.setter
  def window_ratio(self, value):
    """
    Set thermal boundary window ratio
    :param value: str
    """
    if self._window_ratio_is_calculated:
      raise ValueError('Window ratio cannot be assigned when the windows are defined in the geometry.')
    self._window_ratio = float(value)

  @property
  def windows_areas(self) -> [float]:
    """
    Get windows areas
    :return: [float]
    """
    return self._windows_areas

  @property
  def u_value(self) -> Union[None, float]:
    """
    Get thermal boundary U-value in W/m2K
    internal and external convective coefficient in W/m2K values, can be configured at configuration.ini
    :return: None or float
    """
    if self._u_value is None:
      h_i = self.hi
      h_e = self.he
      if self.type == cte.GROUND:
        r_value = 1.0 / h_i + ch().soil_thickness / ch().soil_conductivity
      else:
        r_value = 1.0/h_i + 1.0/h_e
      try:
        for layer in self.layers:
          if layer.material.no_mass:
            r_value += float(layer.material.thermal_resistance)
          else:
            r_value += float(layer.thickness) / float(layer.material.conductivity)
        self._u_value = 1.0/r_value
      except TypeError:
        raise TypeError('Constructions layers are not initialized') from TypeError
    return self._u_value

  @u_value.setter
  def u_value(self, value):
    """
    Set thermal boundary U-value in W/m2K
    :param value: float
    """
    if value is not None:
      self._u_value = float(value)

  @property
  def hi(self) -> Union[None, float]:
    """
    Get internal convective heat transfer coefficient (W/m2K)
    :return: None or float
    """
    return self._hi

  @hi.setter
  def hi(self, value):
    """
    Set internal convective heat transfer coefficient (W/m2K)
    :param value: float
    """
    if value is not None:
      self._hi = value

  @property
  def he(self) -> Union[None, float]:
    """
    Get external convective heat transfer coefficient (W/m2K)
    :return: None or float
    """
    return self._he

  @he.setter
  def he(self, value):
    """
    Set external convective heat transfer coefficient (W/m2K)
    :param value: float
    """
    if value is not None:
      self._he = value

  @property
  def internal_surface(self) -> Surface:
    """
    Get the internal surface of the thermal boundary
    :return: Surface
    """
    if self._internal_surface is None:
      self._internal_surface = self.parent_surface.inverse
    return self._internal_surface
