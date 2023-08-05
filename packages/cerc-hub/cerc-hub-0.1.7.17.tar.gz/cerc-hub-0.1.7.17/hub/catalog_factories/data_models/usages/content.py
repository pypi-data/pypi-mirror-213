"""
Usage catalog usage
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
"""
from hub.catalog_factories.data_models.usages.usage import Usage


class Content:
  """
  Content class
  """
  def __init__(self, usages):
    self._usages = usages

  @property
  def usages(self) -> [Usage]:
    """
    Get catalog usages
    """
    return self._usages
