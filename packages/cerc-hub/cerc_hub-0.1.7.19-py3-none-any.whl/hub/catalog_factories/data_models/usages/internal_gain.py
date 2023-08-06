"""
Usage catalog internal gain
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
"""


class InternalGain:
  """
  InternalGain class
  """

  def __init__(self, internal_gain_type, average_internal_gain, convective_fraction, radiative_fraction, latent_fraction, schedules):
    self._type = internal_gain_type
    self._average_internal_gain = average_internal_gain
    self._convective_fraction = convective_fraction
    self._radiative_fraction = radiative_fraction
    self._latent_fraction = latent_fraction
    self._schedules = schedules
