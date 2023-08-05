"""
Fast charging infrastructure module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""


class FastChargingInfrastructure:
  """
  FastChargingInfrastructure class
  """

  def __init__(self):
    self._electrical_demand = None
    self._losses_in_grid = None

  @property
  def electrical_demand(self):
    """
    Add explanation here
    :return: add type of variable here
    """
    return self._electrical_demand

  @property
  def losses_in_grid(self):
    """
    Add explanation here
    :return: add type of variable here
    """
    return self._losses_in_grid
