"""
Greenery catalog data model Plant percentage class
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
"""

from hub.catalog_factories.data_models.greenery.plant import Plant as HubPlant


class PlantPercentage(HubPlant):
  """
  Plant percentage class
  """

  def __init__(self, percentage, plant_category, plant):
    super().__init__(plant_category, plant)
    self._percentage = percentage

  @property
  def percentage(self):
    """
    Get plant percentage
    :return: float
    """
    return self._percentage
