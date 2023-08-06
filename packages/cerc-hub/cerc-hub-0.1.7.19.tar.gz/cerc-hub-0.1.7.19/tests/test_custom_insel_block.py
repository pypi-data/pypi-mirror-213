"""
TestInselExports test
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
import logging
from pathlib import Path
from unittest import TestCase
import pandas as pd
import hub.helpers.constants as cte
from hub.helpers.monthly_values import MonthlyValues
from hub.imports.geometry_factory import GeometryFactory
from hub.imports.construction_factory import ConstructionFactory
from hub.imports.usage_factory import UsageFactory
from hub.exports.energy_building_exports_factory import EnergyBuildingsExportsFactory
from hub.imports.weather_factory import WeatherFactory


class TestExports(TestCase):
  """
  TestExports class contains the unittest for export functionality
  """
  def setUp(self) -> None:
    """
    Test setup
    :return: None
    """
    self._city = None
    self._complete_city = None
    self._example_path = (Path(__file__).parent / 'tests_data').resolve()
    self._output_path = (Path(__file__).parent / 'tests_outputs').resolve()

  def _get_citygml(self, file):
    file_path = (self._example_path / file).resolve()
    self._city = GeometryFactory('citygml', path=file_path).city
    self.assertIsNotNone(self._city, 'city is none')
    return self._city

  @property
  def _read_sra_file(self) -> []:
    path = (self._example_path / "one_building_in_kelowna_sra_SW.out").resolve()
    _results = pd.read_csv(path, sep='\s+', header=0)
    id_building = ''
    header_building = []
    _radiation = []
    for column in _results.columns.values:
      if id_building != column.split(':')[1]:
        id_building = column.split(':')[1]
        if len(header_building) > 0:
          _radiation.append(pd.concat([MonthlyValues().month_hour, _results[header_building]], axis=1))
        header_building = [column]
      else:
        header_building.append(column)
    _radiation.append(pd.concat([MonthlyValues().month_hour, _results[header_building]], axis=1))
    return _radiation

  def _set_irradiance_surfaces(self, city):
    """
    saves in building surfaces the correspondent irradiance at different time-scales depending on the mode
    if building is None, it saves all buildings' surfaces in file, if building is specified, it saves only that
    specific building values
    :parameter city: city
    :return: none
    """
    city.level_of_detail.surface_radiation = 2
    for radiation in self._read_sra_file:
      city_object_name = radiation.columns.values.tolist()[1].split(':')[1]
      building = city.city_object(city_object_name)
      for column in radiation.columns.values:
        if column == cte.MONTH:
          continue
        header_id = column
        surface_id = header_id.split(':')[2]
        surface = building.surface_by_id(surface_id)
        new_value = pd.DataFrame(radiation[[header_id]].to_numpy(), columns=['sra'])
        surface.global_irradiance[cte.HOUR] = new_value
        month_new_value = MonthlyValues().get_mean_values(new_value)
        surface.global_irradiance[cte.MONTH] = month_new_value

  def test_insel_monthly_energy_balance_export(self):
    """
    export to Insel MonthlyEnergyBalance
    """
    city = self._get_citygml('one_building_in_kelowna.gml')
    WeatherFactory('epw', city).enrich()
    for building in city.buildings:
      building.external_temperature[cte.MONTH] = MonthlyValues().\
        get_mean_values(building.external_temperature[cte.HOUR][['epw']])
    self._set_irradiance_surfaces(city)

    for building in city.buildings:
      self.assertIsNotNone(building.external_temperature[cte.MONTH], f'building {building.name} '
                                                                     f'external_temperature is none')
      for surface in building.surfaces:
        if surface.type != 'Ground':
          self.assertIsNotNone(surface.global_irradiance[cte.MONTH], f'surface in building {building.name} '
                                                                     f'global_irradiance is none')

    for building in city.buildings:
      building.year_of_construction = 2006
      if building.function is None:
        building.function = 'large office'
      building.attic_heated = 0
      building.basement_heated = 0
    ConstructionFactory('nrel', city).enrich()
    UsageFactory('comnet', city).enrich()

    # parameters written:
    for building in city.buildings:
      self.assertIsNotNone(building.volume, f'building {building.name} volume is none')
      self.assertIsNotNone(building.average_storey_height, f'building {building.name} average_storey_height is none')
      self.assertIsNotNone(building.storeys_above_ground, f'building {building.name} storeys_above_ground is none')
      self.assertIsNotNone(building.attic_heated, f'building {building.name} attic_heated is none')
      self.assertIsNotNone(building.basement_heated, f'building {building.name} basement_heated is none')
      for internal_zone in building.internal_zones:
        self.assertIsNotNone(internal_zone.area, f'internal zone {internal_zone.id} area is none')
        for thermal_zone in internal_zone.thermal_zones:
          self.assertIsNotNone(thermal_zone.indirectly_heated_area_ratio, f'thermal zone {thermal_zone.id} '
                                                                          f'indirectly_heated_area_ratio is none')
          self.assertIsNotNone(thermal_zone.effective_thermal_capacity, f'thermal zone {thermal_zone.id} '
                                                                        f'effective_thermal_capacity is none')
          self.assertIsNotNone(thermal_zone.additional_thermal_bridge_u_value, f'thermal zone {thermal_zone.id} '
                                                                               f'additional_thermal_bridge_u_value '
                                                                               f'is none')
          self.assertIsNotNone(thermal_zone.total_floor_area, f'thermal zone {thermal_zone.id} '
                                                              f'total_floor_area is none')
          for thermal_boundary in thermal_zone.thermal_boundaries:
            self.assertIsNotNone(thermal_boundary.type)
            self.assertIsNotNone(thermal_boundary.opaque_area)
            self.assertIsNotNone(thermal_boundary.window_ratio)
            self.assertIsNotNone(thermal_boundary.u_value)
            self.assertIsNotNone(thermal_boundary.thermal_openings)
            if thermal_boundary.type is not cte.GROUND:
              self.assertIsNotNone(thermal_boundary.parent_surface.short_wave_reflectance)

        for usage in internal_zone.usages:
          self.assertIsNotNone(usage.percentage, f'usage zone {usage.name} percentage is none')
          self.assertIsNotNone(usage.internal_gains, f'usage zone {usage.name} internal_gains is none')
          self.assertIsNotNone(usage.thermal_control, f'usage zone {usage.name} thermal_control is none')
          self.assertIsNotNone(usage.hours_day, f'usage zone {usage.name} hours_day is none')
          self.assertIsNotNone(usage.days_year, f'usage zone {usage.name} days_year is none')
          self.assertIsNotNone(
            usage.mechanical_air_change,
            f'usage zone {usage.name} mechanical_air_change is none'
          )
    # export files
    try:
      EnergyBuildingsExportsFactory('insel_monthly_energy_balance', city, self._output_path, 'MEB_Montreal').export()
    except Exception as err:
      logging.exception(err)
      self.fail("Insel MonthlyEnergyBalance ExportsFactory raised ExceptionType unexpectedly!")
