"""
Energy distribution system definition
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from hub.city_model_structure.energy_systems.generic_distribution_system import GenericDistributionSystem


class DistributionSystem:
  """
  DistributionSystem class
  """
  def __init__(self):
    self._generic_distribution_system = None

  @property
  def generic_distribution_system(self) -> GenericDistributionSystem:
    """
    Get generic_distribution_system
    :return: GenericDistributionSystem
    """
    return self._generic_distribution_system

  @generic_distribution_system.setter
  def generic_distribution_system(self, value):
    """
    Set associated generic_distribution_system
    :param value: GenericDistributionSystem
    """
    self._generic_distribution_system = value
