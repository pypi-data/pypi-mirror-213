"""
Energy System catalog content
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""


class Content:
  """
  Content class
  """
  def __init__(self, archetypes, systems, generations, distributions, emissions):
    self._archetypes = archetypes
    self._systems = systems
    self._generations = generations
    self._distributions = distributions
    self._emissions = emissions

  @property
  def archetypes(self):
    """
    All archetype system clusters in the catalog
    """
    return self._archetypes

  @property
  def systems(self):
    """
    All systems in the catalog
    """
    return self._systems

  @property
  def generation_equipments(self):
    """
    All generation equipments in the catalog
    """
    return self._generations

  @property
  def distribution_equipments(self):
    """
    All distribution equipments in the catalog
    """
    return self._distributions

  @property
  def emission_equipments(self):
    """
    All emission equipments in the catalog
    """
    return self._emissions
