"""
Greenery catalog data model Soil class
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
"""


class Soil:
  """
  Soil class
  """
  def __init__(self, soil):
    self._name = soil.name
    self._roughness = soil.roughness
    self._dry_conductivity = soil.conductivityOfDrySoil
    self._dry_density = soil.densityOfDrySoil
    self._dry_specific_heat = soil.specificHeatOfDrySoil
    self._thermal_absorptance = soil.thermalAbsorptance
    self._solar_absorptance = soil.solarAbsorptance
    self._visible_absorptance = soil.visibleAbsorptance
    self._saturation_volumetric_moisture_content = soil.saturationVolumetricMoistureContent
    self._residual_volumetric_moisture_content = soil.residualVolumetricMoistureContent
    self._initial_volumetric_moisture_content = soil.initialVolumetricMoistureContent

  @property
  def name(self):
    """
    Get soil name
    :return: string
    """
    return self._name

  @property
  def roughness(self):
    """
    Get soil roughness
    :return: string
    """
    return self._roughness

  @property
  def dry_conductivity(self):
    """
    Get soil dry conductivity in W/mK
    :return: float
    """
    return self._dry_conductivity

  @property
  def dry_density(self):
    """
    Get soil dry density in kg/m3
    :return: float
    """
    return self._dry_density

  @property
  def dry_specific_heat(self):
    """
    Get soil dry specific heat in J/kgK
    :return: float
    """
    return self._dry_specific_heat

  @property
  def thermal_absorptance(self):
    """
    Get soil thermal absortance
    :return: float
    """
    return self._thermal_absorptance

  @property
  def solar_absorptance(self):
    """
    Get soil solar absortance
    :return: float
    """
    return self._solar_absorptance

  @property
  def visible_absorptance(self):
    """
    Get soil visible absortance
    :return: float
    """
    return self._visible_absorptance

  @property
  def saturation_volumetric_moisture_content(self):
    """
    Get soil saturation volumetric moisture content
    :return: float
    """
    return self._saturation_volumetric_moisture_content

  @property
  def residual_volumetric_moisture_content(self):
    """
    Get soil residual volumetric moisture content
    :return: float
    """
    return self._residual_volumetric_moisture_content

  @property
  def initial_volumetric_moisture_content(self):
    """
    Get soil initial volumetric moisture content
    :return: float
    """
    return self._initial_volumetric_moisture_content
