"""
Construction helper
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from hub.helpers import constants as cte


class ConstructionHelper:
  """
  Construction helper
  """
  # NREL
  _nrel_standards = {
    'ASHRAE Std189': 1,
    'ASHRAE 90.1_2004': 2
  }
  _reference_city_to_nrel_climate_zone = {
    'Miami': 'ASHRAE_2004:1A',
    'Houston': 'ASHRAE_2004:2A',
    'Phoenix': 'ASHRAE_2004:2B',
    'Atlanta': 'ASHRAE_2004:3A',
    'Los Angeles': 'ASHRAE_2004:3B',
    'Las Vegas': 'ASHRAE_2004:3B',
    'San Francisco': 'ASHRAE_2004:3C',
    'Baltimore': 'ASHRAE_2004:4A',
    'Albuquerque': 'ASHRAE_2004:4B',
    'Seattle': 'ASHRAE_2004:4C',
    'Chicago': 'ASHRAE_2004:5A',
    'Boulder': 'ASHRAE_2004:5B',
    'Minneapolis': 'ASHRAE_2004:6A',
    'Helena': 'ASHRAE_2004:6B',
    'Duluth': 'ASHRAE_2004:7A',
    'Fairbanks': 'ASHRAE_2004:8A'
  }
  nrel_window_types = [cte.WINDOW, cte.DOOR, cte.SKYLIGHT]

  nrel_construction_types = {
    cte.WALL: 'exterior wall',
    cte.INTERIOR_WALL: 'interior wall',
    cte.GROUND_WALL: 'ground wall',
    cte.GROUND: 'exterior slab',
    cte.ATTIC_FLOOR: 'attic floor',
    cte.INTERIOR_SLAB: 'interior slab',
    cte.ROOF: 'roof'
  }

  _reference_city_to_nrcan_climate_zone = {
    'Montreal': '6'
  }

  @staticmethod
  def yoc_to_nrel_standard(year_of_construction):
    """
    Year of construction to NREL standard
    :param year_of_construction: int
    :return: str
    """
    if int(year_of_construction) < 2009:
      standard = 'ASHRAE 90.1_2004'
    else:
      standard = 'ASHRAE 189.1_2009'
    return standard

  @staticmethod
  def city_to_reference_city(city):
    """
    City name to reference city
    :param city: str
    :return: str
    """
    # todo: Dummy function that needs to be implemented
    reference_city = 'Montreal'
    if city is not None:
      reference_city = 'Montreal'
    return reference_city

  @staticmethod
  def city_to_nrel_climate_zone(city):
    """
    City name to NREL climate zone
    :param city: str
    :return: str
    """
    reference_city = ConstructionHelper.city_to_reference_city(city)
    if reference_city not in ConstructionHelper._reference_city_to_nrel_climate_zone:
      reference_city = 'Baltimore'
    return ConstructionHelper._reference_city_to_nrel_climate_zone[reference_city]

  @staticmethod
  def city_to_nrcan_climate_zone(city):
    """
    City name to NRCAN climate zone
    :param city: str
    :return: str
    """
    reference_city = ConstructionHelper.city_to_reference_city(city)
    return ConstructionHelper._reference_city_to_nrcan_climate_zone[reference_city]
