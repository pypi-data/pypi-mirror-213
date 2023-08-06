"""
Building module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributors: Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

import logging
from typing import List, Union, TypeVar

import numpy as np
import hub.helpers.constants as cte
from hub.city_model_structure.attributes.polyhedron import Polyhedron
from hub.city_model_structure.building_demand.household import Household
from hub.city_model_structure.building_demand.internal_zone import InternalZone
from hub.city_model_structure.building_demand.thermal_zone import ThermalZone
from hub.city_model_structure.building_demand.surface import Surface
from hub.city_model_structure.city_object import CityObject
from hub.city_model_structure.energy_systems.energy_system import EnergySystem
from hub.helpers.peak_loads import PeakLoads

City = TypeVar('City')


class Building(CityObject):
  """
  Building(CityObject) class
  """
  def __init__(self, name, surfaces, year_of_construction, function, terrains=None, city=None):
    super().__init__(name, surfaces)
    self._city = city
    self._households = None
    self._basement_heated = None
    self._attic_heated = None
    self._terrains = terrains
    self._year_of_construction = year_of_construction
    self._function = function
    self._average_storey_height = None
    self._storeys_above_ground = None
    self._floor_area = None
    self._roof_type = None
    self._internal_zones = None
    self._thermal_zones = None
    self._shell = None
    self._aliases = []
    self._type = 'building'
    self._cold_water_temperature = {}
    self._heating_demand = {}
    self._cooling_demand = {}
    self._lighting_electrical_demand = {}
    self._appliances_electrical_demand = {}
    self._domestic_hot_water_heat_demand = {}
    self._heating_consumption = {}
    self._cooling_consumption = {}
    self._domestic_hot_water_consumption = {}
    self._distribution_systems_electrical_consumption = {}
    self._onsite_electrical_production = {}
    self._eave_height = None
    self._energy_systems = None
    self._systems_archetype_name = None
    self._grounds = []
    self._roofs = []
    self._walls = []
    self._internal_walls = []
    self._ground_walls = []
    self._attic_floors = []
    self._interior_slabs = []
    for surface_id, surface in enumerate(self.surfaces):
      self._min_x = min(self._min_x, surface.lower_corner[0])
      self._min_y = min(self._min_y, surface.lower_corner[1])
      self._min_z = min(self._min_z, surface.lower_corner[2])
      surface.id = surface_id
      if surface.type == cte.GROUND:
        self._grounds.append(surface)
      elif surface.type == cte.WALL:
        self._walls.append(surface)
      elif surface.type == cte.ROOF:
        self._roofs.append(surface)
      elif surface.type == cte.INTERIOR_WALL:
        self._internal_walls.append(surface)
      elif surface.type == cte.GROUND_WALL:
        self._ground_walls.append(surface)
      elif surface.type == cte.ATTIC_FLOOR:
        self._attic_floors.append(surface)
      elif surface.type == cte.INTERIOR_SLAB:
        self._interior_slabs.append(surface)
      else:
        logging.error(f'Building %s [%s] has an unexpected surface type %s.', self.name, self.aliases, surface.type)

  @property
  def shell(self) -> Polyhedron:
    """
    Get building's external polyhedron
    :return: [Polyhedron]
    """
    polygons = []
    for surface in self.surfaces:
      if surface.type is not cte.INTERIOR_WALL:
        polygons.append(surface.solid_polygon)
        if surface.holes_polygons is not None:
          for hole in surface.holes_polygons:
            polygons.append(hole)
    if self._shell is None:
      self._shell = Polyhedron(polygons)
    return self._shell

  @property
  def internal_zones(self) -> List[InternalZone]:
    """
    Get building internal zones
    For Lod up to 3, there is only one internal zone which corresponds to the building shell.
    In LoD 4 there can be more than one. In this case the definition of surfaces and floor area must be redefined.
    :return: [InternalZone]
    """
    if self._internal_zones is None:
      self._internal_zones = [InternalZone(self.surfaces, self.floor_area)]
    return self._internal_zones

  @property
  def thermal_zones(self) -> Union[None, List[ThermalZone]]:
    """
    Get building thermal zones
    For Lod up to 3, there can be more than one thermal zone per internal zone.
    In LoD 4, there can be more than one internal zone, and therefore, only one thermal zone per internal zone
    :return: [ThermalZone]
    """
    if self._thermal_zones is None:
      self._thermal_zones = []
      for internal_zone in self.internal_zones:
        if internal_zone.thermal_zones is None:
          self._thermal_zones = None
          return self._thermal_zones
        for thermal_zone in internal_zone.thermal_zones:
          self._thermal_zones.append(thermal_zone)
    return self._thermal_zones

  @property
  def grounds(self) -> List[Surface]:
    """
    Get building ground surfaces
    :return: [Surface]
    """
    return self._grounds

  @property
  def roofs(self) -> List[Surface]:
    """
    Get building roof surfaces
    :return: [Surface]
    """
    return self._roofs

  @property
  def walls(self) -> List[Surface]:
    """
    Get building wall surfaces
    :return: [Surface]
    """
    return self._walls

  @property
  def internal_walls(self) -> List[Surface]:
    """
    Get building internal wall surfaces
    :return: [Surface]
    """
    return self._internal_walls

  @property
  def terrains(self) -> Union[None, List[Surface]]:
    """
    Get city object terrain surfaces
    :return: [Surface]
    """
    return self._terrains

  @property
  def attic_heated(self) -> Union[None, int]:
    """
    Get if the city object attic is heated
    0: no attic in the building
    1: attic exists but is not heated
    2: attic exists and is heated
    :return: None or int
    """
    return self._attic_heated

  @attic_heated.setter
  def attic_heated(self, value):
    """
    Set if the city object attic is heated
    0: no attic in the building
    1: attic exists but is not heated
    2: attic exists and is heated
    :param value: int
    """
    if value is not None:
      self._attic_heated = int(value)

  @property
  def basement_heated(self) -> Union[None, int]:
    """
    Get if the city object basement is heated
    0: no basement in the building
    1: basement exists but is not heated
    2: basement exists and is heated
    :return: None or int
    """
    return self._basement_heated

  @basement_heated.setter
  def basement_heated(self, value):
    """
    Set if the city object basement is heated
    0: no basement in the building
    1: basement exists but is not heated
    2: basement exists and is heated
    :param value: int
    """
    if value is not None:
      self._basement_heated = int(value)

  @property
  def year_of_construction(self):
    """
    Get building year of construction
    :return: int
    """
    return self._year_of_construction

  @year_of_construction.setter
  def year_of_construction(self, value):
    """
    Set building year of construction
    :param value: int
    """
    if value is not None:
      self._year_of_construction = int(value)

  @property
  def function(self) -> Union[None, str]:
    """
    Get building function
    :return: None or str
    """
    return self._function

  @function.setter
  def function(self, value):
    """
    Set building function
    :param value: str
    """
    if value is not None:
      self._function = str(value)

  @property
  def average_storey_height(self) -> Union[None, float]:
    """
    Get building average storey height in meters
    :return: None or float
    """
    return self._average_storey_height

  @average_storey_height.setter
  def average_storey_height(self, value):
    """
    Set building average storey height in meters
    :param value: float
    """
    if value is not None:
      self._average_storey_height = float(value)

  @property
  def storeys_above_ground(self) -> Union[None, int]:
    """
    Get building storeys number above ground
    :return: None or int
    """
    if self._storeys_above_ground is None:
      if self.eave_height is not None and self.average_storey_height is not None:
        self._storeys_above_ground = int(self.eave_height / self.average_storey_height)
    return self._storeys_above_ground

  @storeys_above_ground.setter
  def storeys_above_ground(self, value):
    """
    Set building storeys number above ground
    :param value: int
    """
    if value is not None:
      self._storeys_above_ground = int(value)

  @property
  def cold_water_temperature(self) -> {float}:
    """
    Get cold water temperature in degrees Celsius
    :return: dict{DataFrame(float)}
    """
    return self._cold_water_temperature

  @cold_water_temperature.setter
  def cold_water_temperature(self, value):
    """
    Set cold water temperature in degrees Celsius
    :param value: dict{DataFrame(float)}
    """
    self._cold_water_temperature = value

  @property
  def heating_demand(self) -> dict:
    """
    Get heating demand in Wh
    :return: dict{DataFrame(float)}
    """
    return self._heating_demand

  @heating_demand.setter
  def heating_demand(self, value):
    """
    Set heating demand in Wh
    :param value: dict{DataFrame(float)}
    """
    self._heating_demand = value

  @property
  def cooling_demand(self) -> dict:
    """
    Get cooling demand in Wh
    :return: dict{DataFrame(float)}
    """
    return self._cooling_demand

  @cooling_demand.setter
  def cooling_demand(self, value):
    """
    Set cooling demand in Wh
    :param value: dict{DataFrame(float)}
    """
    self._cooling_demand = value

  @property
  def lighting_electrical_demand(self) -> dict:
    """
    Get lighting electrical demand in Wh
    :return: dict{DataFrame(float)}
    """
    return self._lighting_electrical_demand

  @lighting_electrical_demand.setter
  def lighting_electrical_demand(self, value):
    """
    Set lighting electrical demand in Wh
    :param value: dict{DataFrame(float)}
    """
    self._lighting_electrical_demand = value

  @property
  def appliances_electrical_demand(self) -> dict:
    """
    Get appliances electrical demand in Wh
    :return: dict{DataFrame(float)}
    """
    return self._appliances_electrical_demand

  @appliances_electrical_demand.setter
  def appliances_electrical_demand(self, value):
    """
    Set appliances electrical demand in Wh
    :param value: dict{DataFrame(float)}
    """
    self._appliances_electrical_demand = value

  @property
  def domestic_hot_water_heat_demand(self) -> dict:
    """
    Get domestic hot water heat demand in Wh
    :return: dict{DataFrame(float)}
    """
    return self._domestic_hot_water_heat_demand

  @domestic_hot_water_heat_demand.setter
  def domestic_hot_water_heat_demand(self, value):
    """
    Set domestic hot water heat demand in Wh
    :param value: dict{DataFrame(float)}
    """
    self._domestic_hot_water_heat_demand = value

  @property
  def heating_peak_load(self) -> Union[None, dict]:
    """
    Get heating peak load in W
    :return: dict{DataFrame(float)}
    """
    results = {}
    if cte.HOUR in self.heating_demand:
      monthly_values = PeakLoads().\
        peak_loads_from_hourly(self.heating_demand[cte.HOUR][next(iter(self.heating_demand[cte.HOUR]))])
    else:
      monthly_values = PeakLoads(self).heating_peak_loads_from_methodology
    if monthly_values is None:
      return None
    results[cte.MONTH] = monthly_values
    results[cte.YEAR] = [max(monthly_values)]
    return results

  @property
  def cooling_peak_load(self) -> Union[None, dict]:
    """
    Get cooling peak load in W
    :return: dict{DataFrame(float)}
    """
    results = {}
    if cte.HOUR in self.cooling_demand:
      monthly_values = PeakLoads().peak_loads_from_hourly(self.cooling_demand[cte.HOUR][next(iter(self.cooling_demand[cte.HOUR]))])
    else:
      monthly_values = PeakLoads(self).cooling_peak_loads_from_methodology
    if monthly_values is None:
      return None
    results[cte.MONTH] = monthly_values
    results[cte.YEAR] = [max(monthly_values)]
    return results

  @property
  def eave_height(self):
    """
    Get building eave height in meters
    :return: float
    """
    if self._eave_height is None:
      self._eave_height = 0
      for wall in self.walls:
        self._eave_height = max(self._eave_height, wall.upper_corner[2]) - self.simplified_polyhedron.min_z
    return self._eave_height

  @property
  def roof_type(self):
    """
    Get roof type for the building flat or pitch
    :return: str
    """
    if self._roof_type is None:
      self._roof_type = 'flat'
      for roof in self.roofs:
        grads = np.rad2deg(roof.inclination)
        if 355 > grads > 5:
          self._roof_type = 'pitch'
          break
    return self._roof_type

  @roof_type.setter
  def roof_type(self, value):
    """
    Set roof type for the building flat or pitch
    :return: str
    """
    self._roof_type = value

  @property
  def floor_area(self):
    """
    Get building floor area in square meters
    :return: float
    """
    if self._floor_area is None:
      self._floor_area = 0
      for surface in self.surfaces:
        if surface.type == 'Ground':
          self._floor_area += surface.perimeter_polygon.area
    return self._floor_area

  @property
  def households(self) -> List[Household]:
    """
    Get the list of households inside the building
    :return: List[Household]
    """
    return self._households

  @property
  def is_conditioned(self):
    """
    Get building heated flag
    :return: Boolean
    """
    if self.internal_zones is None:
      return False
    for internal_zone in self.internal_zones:
      if internal_zone.usages is not None:
        for usage in internal_zone.usages:
          if usage.thermal_control is not None:
            return True
    return False

  @property
  def aliases(self):
    """
    Get the alias name for the building
    :return: str
    """
    return self._aliases

  def add_alias(self, value):
    """
    Add a new alias for the building
    """
    self._aliases.append(value)
    if self.city is not None:
      self.city.add_building_alias(self, value)

  @property
  def city(self) -> City:
    """
    Get the city containing the building
    :return: City
    """
    return self._city

  @city.setter
  def city(self, value):
    """
    Set the city containing the building
    """
    self._city = value

  @property
  def usages_percentage(self):
    """
    Get the usages and percentages for the building
    """
    _usage = ''
    for internal_zone in self.internal_zones:
      if internal_zone.usages is None:
        continue
      for usage in internal_zone.usages:
        _usage = f'{_usage}{usage.name}_{usage.percentage} '
    return _usage.rstrip()

  @property
  def energy_systems(self) -> Union[None, List[EnergySystem]]:
    """
    Get list of energy systems installed to cover the building demands
    :return: [EnergySystem]
    """
    return self._energy_systems

  @energy_systems.setter
  def energy_systems(self, value):
    """
    Set list of energy systems installed to cover the building demands
    :param value: [EnergySystem]
    """
    self._energy_systems = value

  @property
  def energy_systems_archetype_name(self):
    """
    Get energy systems archetype name
    :return: str
    """
    return self._systems_archetype_name

  @energy_systems_archetype_name.setter
  def energy_systems_archetype_name(self, value):
    """
    Set energy systems archetype name
    :param value: str
    """
    self._systems_archetype_name = value

  @property
  def heating_consumption(self):
    """
    Get energy consumption for heating according to the heating system installed in Wh
    return: dict
    """
    if len(self._heating_consumption) == 0:
      for heating_demand_key in self.heating_demand:
        demand = self.heating_demand[heating_demand_key][cte.INSEL_MEB]
        consumption_type = cte.HEATING
        final_energy_consumed = self._calculate_consumption(consumption_type, demand)
        if final_energy_consumed is None:
          continue
        self._heating_consumption[heating_demand_key] = final_energy_consumed
    return self._heating_consumption

  @property
  def cooling_consumption(self):
    """
    Get energy consumption for cooling according to the cooling system installed in Wh
    return: dict
    """
    if len(self._cooling_consumption) == 0:
      for cooling_demand_key in self.cooling_demand:
        demand = self.cooling_demand[cooling_demand_key][cte.INSEL_MEB]
        consumption_type = cte.COOLING
        final_energy_consumed = self._calculate_consumption(consumption_type, demand)
        if final_energy_consumed is None:
          continue
        self._cooling_consumption[cooling_demand_key] = final_energy_consumed
    return self._cooling_consumption

  @property
  def domestic_hot_water_consumption(self):
    """
    Get energy consumption for domestic according to the domestic hot water system installed in Wh
    return: dict
    """
    if len(self._domestic_hot_water_consumption) == 0:
      for domestic_hot_water_demand_key in self.domestic_hot_water_heat_demand:
        demand = self.domestic_hot_water_heat_demand[domestic_hot_water_demand_key][cte.INSEL_MEB]
        consumption_type = cte.DOMESTIC_HOT_WATER
        final_energy_consumed = self._calculate_consumption(consumption_type, demand)
        if final_energy_consumed is None:
          continue
        self._domestic_hot_water_consumption[domestic_hot_water_demand_key] = final_energy_consumed
    return self._domestic_hot_water_consumption

  def _calculate_working_hours(self):
    _working_hours = {}
    for internal_zone in self.internal_zones:
      for thermal_zone in internal_zone.thermal_zones:
        _working_hours_per_thermal_zone = {}
        for schedule in thermal_zone.thermal_control.hvac_availability_schedules:
          _working_hours_per_schedule = [0] * len(schedule.values)
          for i, value in enumerate(schedule.values):
            if value > 0:
              _working_hours_per_schedule[i] = 1
          for day_type in schedule.day_types:
            _working_hours_per_thermal_zone[day_type] = _working_hours_per_schedule
        if len(_working_hours) == 0:
          _working_hours = _working_hours_per_thermal_zone
        else:
          for key, item in _working_hours.items():
            saved_values = _working_hours_per_thermal_zone[key]
            for i, value in enumerate(item):
              _working_hours[key][i] = max(_working_hours[key][i], saved_values[i])

    _total_hours = 0
    for key in _working_hours:
      hours = sum(_working_hours[key])
      _total_hours += hours * cte.DAYS_A_YEAR[key]
    return _total_hours

  @property
  def distribution_systems_electrical_consumption(self):
    """
    Get total electricity consumption for distribution and emission systems in Wh
    return: dict
    """
    if len(self._distribution_systems_electrical_consumption) != 0:
      return self._distribution_systems_electrical_consumption
    _peak_load = self.heating_peak_load[cte.YEAR][0]
    _peak_load_type = cte.HEATING
    if _peak_load < self.cooling_peak_load[cte.YEAR][0]:
      _peak_load = self.cooling_peak_load[cte.YEAR][0]
      _peak_load_type = cte.COOLING

    _working_hours = self._calculate_working_hours()
    _consumption_fix_flow = 0
    if self.energy_systems is None:
      return self._distribution_systems_electrical_consumption
    for energy_system in self.energy_systems:
      emission_system = energy_system.emission_system.generic_emission_system
      parasitic_energy_consumption = 0
      if emission_system is not None:
        parasitic_energy_consumption = emission_system.parasitic_energy_consumption
      distribution_system = energy_system.distribution_system.generic_distribution_system
      consumption_variable_flow = distribution_system.distribution_consumption_variable_flow
      for demand_type in energy_system.demand_types:
        if demand_type.lower() == cte.HEATING.lower():
          if _peak_load_type == cte.HEATING.lower():
            _consumption_fix_flow = distribution_system.distribution_consumption_fix_flow
          for heating_demand_key in self.heating_demand:
            _consumption = [0]*len(self.heating_demand[heating_demand_key][cte.INSEL_MEB])
            _demand = self.heating_demand[heating_demand_key][cte.INSEL_MEB]
            for i, _ in enumerate(_consumption):
              _consumption[i] += (parasitic_energy_consumption + consumption_variable_flow) * _demand[i]
            self._distribution_systems_electrical_consumption[heating_demand_key] = _consumption
        if demand_type.lower() == cte.COOLING.lower():
          if _peak_load_type == cte.COOLING.lower():
            _consumption_fix_flow = distribution_system.distribution_consumption_fix_flow
          for demand_key in self.cooling_demand:
            _consumption = self._distribution_systems_electrical_consumption[demand_key]
            _demand = self.cooling_demand[demand_key][cte.INSEL_MEB]
            for i, _ in enumerate(_consumption):
              _consumption[i] += (parasitic_energy_consumption + consumption_variable_flow) * _demand[i]
            self._distribution_systems_electrical_consumption[demand_key] = _consumption

      for key, item in self._distribution_systems_electrical_consumption.items():
        for i in range(0, len(item)):
          self._distribution_systems_electrical_consumption[key][i] += _peak_load * _consumption_fix_flow \
                                                                       * _working_hours
    return self._distribution_systems_electrical_consumption

  def _calculate_consumption(self, consumption_type, demand):
    # todo: modify when COP depends on the hour
    coefficient_of_performance = 0
    if self.energy_systems is None:
      return None
    for energy_system in self.energy_systems:
      for demand_type in energy_system.demand_types:
        if demand_type.lower() == consumption_type.lower():
          if consumption_type in (cte.HEATING, cte.DOMESTIC_HOT_WATER):
            coefficient_of_performance = energy_system.generation_system.generic_generation_system.heat_efficiency
          elif consumption_type == cte.COOLING:
            coefficient_of_performance = energy_system.generation_system.generic_generation_system.cooling_efficiency
          elif consumption_type == cte.ELECTRICITY:
            coefficient_of_performance = \
              energy_system.generation_system.generic_generation_system.electricity_efficiency
    if coefficient_of_performance == 0:
      values = [0]*len(demand)
      final_energy_consumed = values
    else:
      final_energy_consumed = []
      for demand_value in demand:
        final_energy_consumed.append(demand_value / coefficient_of_performance)
    return final_energy_consumed

  @property
  def onsite_electrical_production(self):
    """
    Get total electricity produced onsite in Wh
    return: dict
    """

    # Add other systems whenever new ones appear
    orientation_losses_factor = {cte.MONTH: {'north': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                             'east': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                             'south': [2.137931, 1.645503, 1.320946, 1.107817, 0.993213, 0.945175,
                                                       0.967949, 1.065534, 1.24183, 1.486486, 1.918033, 2.210526],
                                             'west': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
                                 cte.YEAR: {'north': [0],
                                            'east': [0],
                                            'south': [1.212544],
                                            'west': [0]}
                                 }
    if self.energy_systems is None:
      return self._onsite_electrical_production
    for energy_system in self.energy_systems:
      if energy_system.generation_system.generic_generation_system.type == cte.PHOTOVOLTAIC:
        _efficiency = energy_system.generation_system.generic_generation_system.electricity_efficiency
        self._onsite_electrical_production = {}
        for _key in self.roofs[0].global_irradiance.keys():
          _results = [0 for _ in range(0, len(self.roofs[0].global_irradiance[_key][cte.SRA]))]
          for surface in self.roofs:
            if _key in orientation_losses_factor:
              _results = [x + y * _efficiency * surface.perimeter_area
                          * surface.solar_collectors_area_reduction_factor * z
                          for x, y, z in zip(_results, surface.global_irradiance[_key][cte.SRA],
                                             orientation_losses_factor[_key]['south'])]
          self._onsite_electrical_production[_key] = _results
    return self._onsite_electrical_production
