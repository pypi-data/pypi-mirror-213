"""
Construction catalog content
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
"""


class Content:
  """
  Content class
  """
  def __init__(self, archetypes, constructions, materials, windows):
    self._archetypes = archetypes
    self._constructions = constructions
    self._materials = materials
    self._windows = windows

  @property
  def archetypes(self):
    """
    All archetypes in the catalog
    """
    return self._archetypes

  @property
  def constructions(self):
    """
    All constructions in the catalog
    """
    return self._constructions

  @property
  def materials(self):
    """
    All materials in the catalog
    """
    return self._materials

  @property
  def windows(self):
    """
    All windows in the catalog
    """
    return self._windows
