"""
Cost catalog content
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Atiya atiya.atiya@mail.concordia.ca
Code contributors: Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""


class Content:
  """
  Content class
  """
  def __init__(self, archetypes):
    self._archetypes = archetypes

  @property
  def archetypes(self):
    """
    All archetypes in the catalog
    """
    return self._archetypes
