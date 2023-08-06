"""
Energy System catalog archetype
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from typing import List

from hub.catalog_factories.data_models.energy_systems.system import System


class Archetype:
  """
  Archetype class
  """
  def __init__(self, lod, name, systems):

    self._lod = lod
    self._name = name
    self._systems = systems

  @property
  def lod(self):
    """
    Get level of detail of the catalog
    :return: string
    """
    return self._lod

  @property
  def name(self):
    """
    Get name
    :return: string
    """
    return f'{self._name}_lod{self._lod}'

  @property
  def systems(self) -> List[System]:
    """
    Get list of equipments that compose the total energy system
    :return: [Equipment]
    """
    return self._systems
