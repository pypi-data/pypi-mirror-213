"""
ConstructionFactory (before PhysicsFactory) retrieve the specific construction module for the given region
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributors: Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from hub.helpers.utils import validate_import_export_type
from hub.imports.construction.nrcan_physics_parameters import NrcanPhysicsParameters
from hub.imports.construction.nrel_physics_parameters import NrelPhysicsParameters


class ConstructionFactory:
  """
  ConstructionFactory class
  """
  def __init__(self, handler, city):
    self._handler = '_' + handler.lower()
    validate_import_export_type(ConstructionFactory, handler)
    self._city = city

  def _nrel(self):
    """
    Enrich the city by using NREL information
    """
    NrelPhysicsParameters(self._city).enrich_buildings()
    self._city.level_of_detail.construction = 2
    for building in self._city.buildings:
      building.level_of_detail.construction = 2

  def _nrcan(self):
    """
    Enrich the city by using NRCAN information
    """
    NrcanPhysicsParameters(self._city).enrich_buildings()
    self._city.level_of_detail.construction = 2
    for building in self._city.buildings:
      building.level_of_detail.construction = 2

  def enrich(self):
    """
    Enrich the city given to the class using the class given handler
    :return: None
    """
    getattr(self, self._handler, lambda: None)()
