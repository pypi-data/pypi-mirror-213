"""
TestCityMerge test and validate the merge of several cities into one
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez Guillermo.GutierrezMorote@concordia.ca
"""
import copy
import distutils.spawn
import subprocess
from pathlib import Path
from unittest import TestCase

import pandas as pd

from hub.city_model_structure.city import City
from hub.imports.geometry_factory import GeometryFactory
from hub.imports.results_factory import ResultFactory
from hub.exports.exports_factory import ExportsFactory
import hub.helpers.constants as cte


class TestCityMerge(TestCase):
  """
  Functional TestCityMerge
  """
  def setUp(self) -> None:
    """
    Test setup
    :return: None
    """
    self._example_path = (Path(__file__).parent / 'tests_data').resolve()
    self._output_path = (Path(__file__).parent / 'tests_outputs').resolve()
    self._executable = 'sra'

  def test_merge(self):
    file_path = Path('./tests_data/test.geojson').resolve()
    full_city = GeometryFactory('geojson', file_path, height_field='citygml_me').city
    self.assertEqual(17, len(full_city.buildings), 'Wrong number of buildings')
    odd_city = City(full_city.lower_corner, full_city.upper_corner, full_city.srs_name)
    par_city = City(full_city.lower_corner, full_city.upper_corner, full_city.srs_name)
    for building in full_city.buildings:
      if int(building.name) % 2 == 0:
        par_city.add_city_object(copy.deepcopy(building))
      else:
        odd_city.add_city_object(copy.deepcopy(building))
    self.assertEqual(8, len(odd_city.buildings), 'Wrong number of odd buildings')
    self.assertEqual(9, len(par_city.buildings), 'Wrong number of par buildings')
    merged_city = odd_city.merge(par_city)
    self.assertEqual(17, len(merged_city.buildings), 'Wrong number of buildings in merged city')
    merged_city = par_city.merge(odd_city)
    self.assertEqual(17, len(merged_city.buildings), 'Wrong number of buildings in merged city')
    merged_city = full_city.merge(odd_city).merge(par_city)
    self.assertEqual(17, len(merged_city.buildings), 'Wrong number of buildings in merged city')

  def test_merge_with_radiation(self):
    sra = distutils.spawn.find_executable('sra')
    file_path = Path('./tests_data/test.geojson').resolve()
    output_path = Path('./tests_outputs/')
    full_city = GeometryFactory('geojson', file_path, height_field='citygml_me').city
    par_city = City(full_city.lower_corner, full_city.upper_corner, full_city.srs_name)
    for building in full_city.buildings:
      if int(building.name) % 2 == 0:
        par_city.add_city_object(copy.deepcopy(building))
    ExportsFactory('sra', full_city, output_path).export()
    sra_file = str((output_path / f'{full_city.name}_sra.xml').resolve())
    subprocess.run([sra, sra_file], stdout=subprocess.DEVNULL)
    ResultFactory('sra', full_city, output_path).enrich()
    self.assertEqual(17, len(full_city.buildings), 'Wrong number of buildings')
    merged_city = full_city.merge(par_city)
    merged_city_building_total_radiation = 0
    for building in merged_city.buildings:
      for surface in building.surfaces:
        if surface.global_irradiance:
          merged_city_building_total_radiation += surface.global_irradiance[cte.YEAR].iloc[0, 0]
    self.assertEqual(447383461, merged_city_building_total_radiation)
    merged_city = par_city.merge(full_city)
    merged_city_building_total_radiation = 0
    for building in merged_city.buildings:
      for surface in building.surfaces:
        if surface.global_irradiance:
          merged_city_building_total_radiation += surface.global_irradiance[cte.YEAR].iloc[0, 0]
    self.assertEqual(447383461, merged_city_building_total_radiation)

    for building in par_city.buildings:
      for surface in building.surfaces:
        surface.global_irradiance[cte.YEAR] = pd.DataFrame([3], columns=['sra_mockup_value'])

    merged_city = full_city.merge(par_city)
    merged_city_building_total_radiation = 0
    for building in merged_city.buildings:
      for surface in building.surfaces:
        if surface.global_irradiance:
          merged_city_building_total_radiation += surface.global_irradiance[cte.YEAR].iloc[0, 0]
    self.assertEqual(202699159, merged_city_building_total_radiation)
    merged_city = par_city.merge(full_city)
    merged_city_building_total_radiation = 0
    for building in merged_city.buildings:
      for surface in building.surfaces:
        if surface.global_irradiance:
          merged_city_building_total_radiation += surface.global_irradiance[cte.YEAR].iloc[0, 0]
    self.assertEqual(202699159, merged_city_building_total_radiation)

