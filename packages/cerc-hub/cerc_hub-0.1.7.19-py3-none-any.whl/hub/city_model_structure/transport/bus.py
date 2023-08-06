"""
Bus module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from hub.city_model_structure.attributes.schedule import Schedule


class Bus:
  """
  Bus class
  """

  def __init__(self):
    self._maintenance_time = None
    self._charging_time = None
    self._recovery_time = None
    self._vehicle_type = None
    self._energy_consumption = None
    self._trips_schedule = None
    self._capacity = None
    self._maintenance_cost = None
    self._investment_cost = None
    self._charging_range = None
    self._maximum_travel_range = None

  @property
  def maintenance_time(self):
    """
    Add explanation here
    :return: add type of variable here
    """
    return self._maintenance_time

  @property
  def charging_time(self):
    """
    Add explanation here
    :return: add type of variable here
    """
    return self._charging_time

  @property
  def recovery_time(self):
    """
    Add explanation here
    :return: add type of variable here
    """
    return self.maintenance_time + self.charging_time

  @property
  def vehicle_type(self):
    """
    Add explanation here
    :return: add type of variable here
    """
    return self._vehicle_type

  @property
  def energy_consumption(self):
    """
    Add explanation here
    :return: add type of variable here
    """
    return self._energy_consumption

  @property
  def trips_schedule(self) -> Schedule:
    """
    Add explanation here
    :return: add type of variable here
    """
    return self._trips_schedule

  @property
  def capacity(self):
    """
    Add explanation here
    :return: add type of variable here
    """
    return self._capacity

  @property
  def maintenance_cost(self):
    """
    Add explanation here
    :return: add type of variable here
    """
    return self._maintenance_cost

  @property
  def investment_cost(self):
    """
    Add explanation here
    :return: add type of variable here
    """
    return self._investment_cost

  @property
  def charging_range(self):
    """
    Add explanation here
    :return: add type of variable here
    """
    return self._charging_range

  @property
  def maximum_travel_range(self):
    """
    Add explanation here
    :return: add type of variable here
    """
    return self._maximum_travel_range
