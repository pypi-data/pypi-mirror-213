"""
EnergyBuildingsExportsFactory exports a city into several formats related to energy in buildings
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de uribarri pilar.monsalvete@concordia.ca
"""

from pathlib import Path

from hub.exports.building_energy.energy_ade import EnergyAde
from hub.exports.building_energy.idf import Idf
from hub.exports.building_energy.insel.insel_monthly_energy_balance import InselMonthlyEnergyBalance
from hub.helpers.utils import validate_import_export_type


class EnergyBuildingsExportsFactory:
  """
  Energy Buildings exports factory class
  """
  def __init__(self, handler, city, path, custom_insel_block='d18599', target_buildings=None):
    self._city = city
    self._export_type = '_' + handler.lower()
    validate_import_export_type(EnergyBuildingsExportsFactory, handler)
    if isinstance(path, str):
      path = Path(path)
    self._path = path
    self._custom_insel_block = custom_insel_block
    self._target_buildings = target_buildings

  @property
  def _energy_ade(self):
    """
    Export to citygml with application domain extensions
    :return: None
    """
    return EnergyAde(self._city, self._path)

  @property
  def _idf(self):
    """
    Export the city to Energy+ idf format

    When target_buildings is set, only those will be calculated and their energy consumption output, non-adjacent
    buildings will be considered shading objects and adjacent buildings will be considered adiabatic.

    Adjacent buildings are provided they will be considered heated so energy plus calculations are more precise but
    no results will be calculated to speed up the calculation process.

    :return: None
    """
    idf_data_path = (Path(__file__).parent / './building_energy/idf_files/').resolve()
    # todo: create a get epw file function based on the city
    weather_path = (Path(__file__).parent / '../data/weather/epw/CAN_PQ_Montreal.Intl.AP.716270_CWEC.epw').resolve()
    return Idf(self._city, self._path, (idf_data_path / 'Minimal.idf'), (idf_data_path / 'Energy+.idd'), weather_path,
               target_buildings=self._target_buildings)

  @property
  def _insel_monthly_energy_balance(self):
    """
    Export to Insel MonthlyEnergyBalance
    :return: None
    """
    return InselMonthlyEnergyBalance(self._city, self._path, self._custom_insel_block)

  def export(self):
    """
    Export the city given to the class using the given export type handler
    :return: None
    """
    return getattr(self, self._export_type, lambda: None)
