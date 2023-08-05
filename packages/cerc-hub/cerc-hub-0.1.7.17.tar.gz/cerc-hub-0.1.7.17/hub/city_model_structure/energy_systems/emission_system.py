"""
Energy emission system definition
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from hub.city_model_structure.energy_systems.generic_emission_system import GenericEmissionSystem


class EmissionSystem:
  """
  EmissionSystem class
  """
  def __init__(self):
    self._generic_emission_system = None

  @property
  def generic_emission_system(self) -> GenericEmissionSystem:
    """
    Get associated generic_emission_system
    :return: GenericEmissionSystem
    """
    return self._generic_emission_system

  @generic_emission_system.setter
  def generic_emission_system(self, value):
    """
    Set associated
    :param value: GenericEmissionSystem
    """
    self._generic_emission_system = value
