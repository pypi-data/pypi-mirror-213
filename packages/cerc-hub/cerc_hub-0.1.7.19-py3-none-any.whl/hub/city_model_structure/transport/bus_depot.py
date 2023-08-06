"""
Bus depot module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from hub.city_model_structure.transport.bus_node import BusNode


class BusDepot(BusNode):
  """
  BusDepot class
  """

  def __init__(self, name, coordinates, edges=None):
    super().__init__(name, coordinates, edges=edges, node_type='BusDepot')
    self._number_of_charging_poles = None
    self._number_of_available_buses = None

  @property
  def number_of_charging_poles(self):
    """
    Add explanation here
    :return: add type of variable here
    """
    return self._number_of_charging_poles

  @property
  def number_of_available_buses(self):
    """
    Add explanation here
    :return: add type of variable here
    """
    return self._number_of_available_buses
