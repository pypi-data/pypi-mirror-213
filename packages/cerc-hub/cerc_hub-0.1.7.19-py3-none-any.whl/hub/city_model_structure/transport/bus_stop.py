"""
Bus stop module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from typing import Union
from hub.city_model_structure.transport.bus_node import BusNode
from hub.city_model_structure.transport.fast_charging_infrastructure import FastChargingInfrastructure
from hub.city_model_structure.attributes.schedule import Schedule


class BusStop(BusNode):
  """
  BusStop class
  """

  def __init__(self, name, coordinates, edges=None):
    super().__init__(name, coordinates, edges=edges, node_type='BusStop')
    self._time_table = None
    self._average_hourly_passengers_demand = None
    self._fast_charging_infrastructure = None
    self._waiting_time = None

  @property
  def time_table(self):
    """
    Add explanation here
    :return: add type of variable here
    """
    return self._time_table

  @property
  def average_hourly_passengers_demand(self) -> Schedule:
    """
    Add explanation here
    :return: Schedule
    """
    return self._average_hourly_passengers_demand

  @property
  def fast_charging_infrastructure(self) -> Union[None, FastChargingInfrastructure]:
    """
    Add explanation here
    :return: FastChargingInfrastructure
    """
    return self._fast_charging_infrastructure

  @property
  def waiting_time(self):
    """
    Add explanation here
    :return: add type of variable here
    """
    return self._waiting_time
