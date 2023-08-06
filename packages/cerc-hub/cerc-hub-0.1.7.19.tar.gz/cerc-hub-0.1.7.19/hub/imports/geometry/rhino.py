"""
Rhino module parses rhino files and import the geometry into the city model structure
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.capip
"""
import numpy as np
from rhino3dm import *
from rhino3dm._rhino3dm import Extrusion, MeshType, File3dm

from hub.city_model_structure.attributes.point import Point
from hub.city_model_structure.attributes.polygon import Polygon
from hub.city_model_structure.building import Building
from hub.city_model_structure.building_demand.surface import Surface as HubSurface
from hub.city_model_structure.city import City
from hub.helpers.configuration_helper import ConfigurationHelper
from hub.imports.geometry.helpers.geometry_helper import GeometryHelper


class Rhino:
  """
  Rhino class
  """
  def __init__(self, path):
    self._model = File3dm.Read(str(path))
    max_float = float(ConfigurationHelper().max_coordinate)
    min_float = float(ConfigurationHelper().min_coordinate)
    self._min_x = self._min_y = self._min_z = max_float
    self._max_x = self._max_y = self._max_z = min_float

  @staticmethod
  def _in_perimeter(wall, corner):
    res = wall.contains_point(Point(corner))
    return res

  @staticmethod
  def _add_hole(solid_polygon, hole):
    first = solid_polygon.points[0]
    points = first + hole.points + solid_polygon.points
    return Polygon(points)

  @staticmethod
  def _solid_points(coordinates) -> np.ndarray:
    solid_points = np.fromstring(coordinates, dtype=float, sep=' ')
    solid_points = GeometryHelper.to_points_matrix(solid_points)

    result = []
    found = False
    for row in solid_points:
      for row2 in result:
        if row[0] == row2[0] and row[1] == row2[1] and row[2] == row2[2]:
          found = True
      if not found:
        result.append(row)
    return solid_points

  def _corners(self, point):
    if point.X < self._min_x:
      self._min_x = point.X
    if point.Y < self._min_y:
      self._min_y = point.Y
    if point.Z < self._min_z:
      self._min_z = point.Z
    if point.X > self._max_x:
      self._max_x = point.X
    if point.Y > self._max_y:
      self._max_y = point.Y
    if point.Z > self._max_z:
      self._max_z = point.Z

  def _add_face(self, face):
    hub_surfaces = []
    _mesh = face.GetMesh(MeshType.Default)
    for i in range(0, len(_mesh.Faces)):
      mesh_faces = _mesh.Faces[i]
      _points = ''
      faces = []
      for index in mesh_faces:
        if index in faces:
          continue
        faces.append(index)
        self._corners(_mesh.Vertices[index])
        _points = _points + f'{_mesh.Vertices[index].X} {_mesh.Vertices[index].Y} {_mesh.Vertices[index].Z} '
      polygon_points = Rhino._solid_points(_points.strip())
      hub_surfaces.append(HubSurface(Polygon(polygon_points), Polygon(polygon_points)))
    return hub_surfaces

  @property
  def city(self) -> City:
    """
    Return a city based in the rhino file
    :return: City
    """
    buildings = []
    city_objects = []  # building and "windows"
    windows = []
    _prev_name = ''

    for obj in self._model.Objects:
      name = obj.Attributes.Id
      hub_surfaces = []
      if isinstance(obj.Geometry, Extrusion):
        surface = obj.Geometry
        hub_surfaces = hub_surfaces + self._add_face(surface)
      else:
        for face in obj.Geometry.Faces:
          if face is None:
            break
          hub_surfaces = hub_surfaces + self._add_face(face)
      building = Building(name, hub_surfaces, 'unknown', 'unknown', [])
      city_objects.append(building)
    lower_corner = (self._min_x, self._min_y, self._min_z)
    upper_corner = (self._max_x, self._max_y, self._max_z)
    city = City(lower_corner, upper_corner, 'EPSG:26918')
    for building in city_objects:
      if len(building.surfaces) <= 2:
        # is not a building but a window!
        for surface in building.surfaces:
          # add to windows the "hole" with the normal inverted
          windows.append(Polygon(surface.perimeter_polygon.inverse))
      else:
        buildings.append(building)

    # todo: this method will be pretty inefficient
    for hole in windows:
      corner = hole.coordinates[0]
      for building in buildings:
        for surface in building.surfaces:
          plane = surface.perimeter_polygon.plane
          # todo: this is a hack for dompark project it should not be done this way windows should be correctly modeled
          # if the distance between the wall plane and the window is less than 2m
          # and the window Z coordinate it's between the wall Z, it's a window of that wall
          if plane.distance_to_point(corner) <= 2:
            # check if the window is in the right high.
            if surface.upper_corner[2] >= corner[2] >= surface.lower_corner[2]:
              if surface.holes_polygons is None:
                surface.holes_polygons = []
              surface.holes_polygons.append(hole)

    for building in buildings:
      city.add_city_object(building)
      building.level_of_detail.geometry = 3
    city.level_of_detail.geometry = 3
    return city
