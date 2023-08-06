"""
Join module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
Code contributors: Guille guille.gutierrezmorote@concordia.ca
"""

from hub.city_model_structure.transport.traffic_node import TrafficNode


class Join(TrafficNode):
  """
  Join class
  """

  def __init__(self, name, coordinates, nodes):
    self._nodes = nodes
    edges = []
    prohibitions = []
    connections = []
    for node in self._nodes:
      edges = edges + node.edges
      prohibitions = prohibitions + node.prohibitions
      connections = connections + node.connections
    super().__init__(name, coordinates, edges=edges, prohibitions=prohibitions, connections=connections,
                     node_type='Join')
