"""
NrelPhysicsParameters import the construction and material information defined by NREL
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributors: Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
import logging

from hub.catalog_factories.construction_catalog_factory import ConstructionCatalogFactory
from hub.city_model_structure.building_demand.layer import Layer
from hub.city_model_structure.building_demand.material import Material
from hub.helpers.dictionaries import Dictionaries
from hub.imports.construction.helpers.construction_helper import ConstructionHelper
from hub.imports.construction.helpers.storeys_generation import StoreysGeneration


class NrelPhysicsParameters:
  """
  NrelPhysicsParameters class
  """

  def __init__(self, city, divide_in_storeys=False):
    self._city = city
    self._divide_in_storeys = divide_in_storeys
    self._climate_zone = ConstructionHelper.city_to_nrel_climate_zone(city.name)

  def enrich_buildings(self):
    """
    Returns the city with the construction parameters assigned to the buildings
    """
    city = self._city
    nrel_catalog = ConstructionCatalogFactory('nrel').catalog
    for building in city.buildings:
      if building.function not in Dictionaries().hub_function_to_nrel_construction_function:
        logging.error(f'Building %s has unknown function %s', building.name, building.function)
        continue
      function = Dictionaries().hub_function_to_nrel_construction_function[building.function]
      try:
        archetype = self._search_archetype(nrel_catalog, function, building.year_of_construction, self._climate_zone)
      except KeyError:
        logging.error(f'Building {building.name} has unknown construction archetype for building function: {function} '
                      f'[{building.function}], building year of construction: {building.year_of_construction}'
                      f' and climate zone {self._climate_zone}\n')

        continue
      # if building has no thermal zones defined from geometry, and the building will be divided in storeys,
      # one thermal zone per storey is assigned
      if len(building.internal_zones) == 1:
        if building.internal_zones[0].thermal_zones is None:
          self._create_storeys(building, archetype, self._divide_in_storeys)
        if self._divide_in_storeys:
          for internal_zone in building.internal_zones:
            for thermal_zone in internal_zone.thermal_zones:
              thermal_zone.total_floor_area = thermal_zone.footprint_area
        else:
          number_of_storeys = int(building.eave_height / building.average_storey_height)
          thermal_zone = building.internal_zones[0].thermal_zones[0]
          thermal_zone.total_floor_area = thermal_zone.footprint_area * number_of_storeys
      else:
        for internal_zone in building.internal_zones:
          for thermal_zone in internal_zone.thermal_zones:
            thermal_zone.total_floor_area = thermal_zone.footprint_area

      for internal_zone in building.internal_zones:
        self._assign_values(internal_zone.thermal_zones, archetype)
        for thermal_zone in internal_zone.thermal_zones:
          self._calculate_view_factors(thermal_zone)

  @staticmethod
  def _search_archetype(nrel_catalog, function, year_of_construction, climate_zone):
    nrel_archetypes = nrel_catalog.entries('archetypes')
    for building_archetype in nrel_archetypes:
      construction_period_limits = building_archetype.construction_period.split(' - ')
      if construction_period_limits[1] == 'PRESENT':
        construction_period_limits[1] = 3000
      if int(construction_period_limits[0]) <= int(year_of_construction) < int(construction_period_limits[1]):
        if str(function) == str(building_archetype.function) and climate_zone == str(building_archetype.climate_zone):
          return building_archetype
    raise KeyError('archetype not found')

  @staticmethod
  def _search_construction_in_archetype(archetype, construction_type):
    construction_archetypes = archetype.constructions
    for construction_archetype in construction_archetypes:
      if str(construction_type) == str(construction_archetype.type):
        return construction_archetype
    return None

  def _assign_values(self, thermal_zones, archetype):
    for thermal_zone in thermal_zones:
      thermal_zone.additional_thermal_bridge_u_value = archetype.extra_loses_due_to_thermal_bridges
      thermal_zone.effective_thermal_capacity = archetype.thermal_capacity
      thermal_zone.indirectly_heated_area_ratio = archetype.indirect_heated_ratio
      thermal_zone.infiltration_rate_system_on = archetype.infiltration_rate_for_ventilation_system_on
      thermal_zone.infiltration_rate_system_off = archetype.infiltration_rate_for_ventilation_system_off
      for thermal_boundary in thermal_zone.thermal_boundaries:
        construction_archetype = self._search_construction_in_archetype(archetype, thermal_boundary.type)
        thermal_boundary.construction_name = construction_archetype.name
        try:
          thermal_boundary.window_ratio = construction_archetype.window_ratio
        except ValueError:
          # This is the normal operation way when the windows are defined in the geometry
          continue
        thermal_boundary.layers = []
        for layer_archetype in construction_archetype.layers:
          layer = Layer()
          layer.thickness = layer_archetype.thickness
          material = Material()
          archetype_material = layer_archetype.material
          material.name = archetype_material.name
          material.id = archetype_material.id
          material.no_mass = archetype_material.no_mass
          if archetype_material.no_mass:
            material.thermal_resistance = archetype_material.thermal_resistance
          else:
            material.density = archetype_material.density
            material.conductivity = archetype_material.conductivity
            material.specific_heat = archetype_material.specific_heat
          material.solar_absorptance = archetype_material.solar_absorptance
          material.thermal_absorptance = archetype_material.thermal_absorptance
          material.visible_absorptance = archetype_material.visible_absorptance
          layer.material = material
          thermal_boundary.layers.append(layer)
        # The agreement is that the layers are defined from outside to inside
        external_layer = construction_archetype.layers[0]
        external_surface = thermal_boundary.parent_surface
        external_surface.short_wave_reflectance = 1 - external_layer.material.solar_absorptance
        external_surface.long_wave_emittance = 1 - external_layer.material.solar_absorptance
        internal_layer = construction_archetype.layers[len(construction_archetype.layers) - 1]
        internal_surface = thermal_boundary.internal_surface
        internal_surface.short_wave_reflectance = 1 - internal_layer.material.solar_absorptance
        internal_surface.long_wave_emittance = 1 - internal_layer.material.solar_absorptance

        for thermal_opening in thermal_boundary.thermal_openings:
          if construction_archetype.window is not None:
            window_archetype = construction_archetype.window
            thermal_opening.construction_name = window_archetype.name
            thermal_opening.frame_ratio = window_archetype.frame_ratio
            thermal_opening.g_value = window_archetype.g_value
            thermal_opening.overall_u_value = window_archetype.overall_u_value

  # todo: verify windows
  @staticmethod
  def _calculate_view_factors(thermal_zone):
    """
    Get thermal zone view factors matrix
    :return: [[float]]
    """
    total_area = 0
    for thermal_boundary in thermal_zone.thermal_boundaries:
      total_area += thermal_boundary.opaque_area
      for thermal_opening in thermal_boundary.thermal_openings:
        total_area += thermal_opening.area

    view_factors_matrix = []
    for thermal_boundary_1 in thermal_zone.thermal_boundaries:
      values = []
      for thermal_boundary_2 in thermal_zone.thermal_boundaries:
        value = 0
        if thermal_boundary_1.id != thermal_boundary_2.id:
          value = thermal_boundary_2.opaque_area / (total_area - thermal_boundary_1.opaque_area)
        values.append(value)
      for thermal_boundary in thermal_zone.thermal_boundaries:
        for thermal_opening in thermal_boundary.thermal_openings:
          value = thermal_opening.area / (total_area - thermal_boundary_1.opaque_area)
          values.append(value)
      view_factors_matrix.append(values)

    for thermal_boundary_1 in thermal_zone.thermal_boundaries:
      values = []
      for thermal_opening_1 in thermal_boundary_1.thermal_openings:
        for thermal_boundary_2 in thermal_zone.thermal_boundaries:
          value = thermal_boundary_2.opaque_area / (total_area - thermal_opening_1.area)
          values.append(value)
        for thermal_boundary in thermal_zone.thermal_boundaries:
          for thermal_opening_2 in thermal_boundary.thermal_openings:
            value = 0
            if thermal_opening_1.id != thermal_opening_2.id:
              value = thermal_opening_2.area / (total_area - thermal_opening_1.area)
            values.append(value)
        view_factors_matrix.append(values)
    thermal_zone.view_factors_matrix = view_factors_matrix

  @staticmethod
  def _create_storeys(building, archetype, divide_in_storeys):
    building.average_storey_height = archetype.average_storey_height
    thermal_zones = StoreysGeneration(building, building.internal_zones[0],
                                      divide_in_storeys=divide_in_storeys).thermal_zones
    building.internal_zones[0].thermal_zones = thermal_zones
