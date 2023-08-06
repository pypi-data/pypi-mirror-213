"""
export a city into Obj format
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
"""

from pathlib import Path


class Obj:
  """
  Export to obj format
  """
  def __init__(self, city, path):
    self._city = city
    self._path = path
    self._export()

  def _to_vertex(self, coordinate):
    x = coordinate[0] - self._city.lower_corner[0]
    y = coordinate[1] - self._city.lower_corner[1]
    z = coordinate[2] - self._city.lower_corner[2]
    return f'v {x} {y} {z}\n'

  def _export(self):
    if self._city.name is None:
      self._city.name = 'unknown_city'
    file_name = self._city.name + '.obj'
    file_path = (Path(self._path).resolve() / file_name).resolve()
    vertices = {}
    with open(file_path, 'w', encoding='utf-8') as obj:
      obj.write("# cerc-hub export\n")
      vertex_index = 0
      faces = []
      for building in self._city.buildings:
        obj.write(f'# building {building.name}\n')
        obj.write(f'g {building.name}\n')
        obj.write('s off\n')
        for surface in building.surfaces:
          obj.write(f'# surface {surface.name}\n')
          face = 'f '
          for coordinate in surface.perimeter_polygon.coordinates:
            vertex = self._to_vertex(coordinate)
            if vertex not in vertices:
              vertex_index += 1
              vertices[vertex] = vertex_index
              current = vertex_index
              obj.write(vertex)
            else:
              current = vertices[vertex]

            face = f'{face} {current}'

          faces.append(f'{face} {face.split(" ")[1]}\n')
          obj.writelines(faces)
          faces = []
