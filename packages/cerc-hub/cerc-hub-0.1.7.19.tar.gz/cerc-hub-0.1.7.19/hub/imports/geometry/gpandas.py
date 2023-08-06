"""
gpandas module parses geopandas input table and import the geometry into the city model structure
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder:  Milad Aghamohamadnia --- milad.aghamohamadnia@concordia.ca
"""

import trimesh
import trimesh.exchange.load
import trimesh.geometry
import trimesh.creation
import trimesh.repair
from shapely.geometry import Point
from shapely.geometry import Polygon as ShapelyPoly
from trimesh import Scene

from hub.city_model_structure.attributes.polygon import Polygon
from hub.city_model_structure.building import Building
from hub.city_model_structure.building_demand.surface import Surface
from hub.city_model_structure.city import City

import hub.helpers.constants as cte


class GPandas:
  """
  GeoPandas class
  """

  def __init__(self, dataframe, srs_name='EPSG:26911'):
    """_summary_
    Arguments:
      dataframe {Geopandas.Dataframe} -- input geometry data in geopandas table
    Keyword Arguments:
      srs_name {str} -- coordinate system of coordinate system (default: {'EPSG:26911'})
    """

    self._srs_name = srs_name
    self._city = None
    self._scene = dataframe
    self._scene = self._scene.to_crs(self._srs_name)
    min_x, min_y, max_x, max_y = self._scene.total_bounds
    self._lower_corner = [min_x, min_y, 0]
    self._upper_corner = [max_x, max_y, 0]

  @property
  def scene(self) -> Scene:
    """
    Get GeoPandas scene
    """
    return self._scene

  @property
  def city(self) -> City:
    """
    Get city out of a GeoPandas Table
    """
    if self._city is None:
      self._city = City(self._lower_corner, self._upper_corner, self._srs_name)
      lod = 0
      for _, bldg in self._scene.iterrows():
        polygon = bldg.geometry
        height = float(bldg['height'])
        building_mesh = trimesh.creation.extrude_polygon(polygon, height)
        trimesh.repair.fill_holes(building_mesh)
        trimesh.repair.fix_winding(building_mesh)
        year_of_construction = int(bldg['year_built'])
        name = bldg['name']
        lod = 1
        if year_of_construction > 2000:
          function = cte.RESIDENTIAL
        else:
          function = cte.INDUSTRY
        surfaces = []
        for _, face in enumerate(building_mesh.faces):
          points = []
          for vertex_index in face:
            points.append(building_mesh.vertices[vertex_index])
          solid_polygon = Polygon(points)
          perimeter_polygon = solid_polygon
          surface = Surface(solid_polygon, perimeter_polygon)
          surfaces.append(surface)
        building = Building(name, surfaces, year_of_construction, function, terrains=None)
        self._city.add_city_object(building)
      self._city.level_of_detail.geometry = lod
      for building in self._city.buildings:
        building.level_of_detail.geometry = lod
    return self._city

  @staticmethod
  def resize_polygon(poly, factor=0.10, expand=False) -> ShapelyPoly:
    """
    returns the shapely polygon which is smaller or bigger by passed factor.
    Arguments:
    poly {shapely.geometry.Polygon} -- an input geometry in shapely polygon format

    Keyword Arguments:
      factor {float} -- factor of expansion (default: {0.10})
      expand {bool} -- If expand = True , then it returns bigger polygon, else smaller (default: {False})

    Returns:
      {shapely.geometry.Polygon} -- output geometry in shapely polygon format
    """
    xs = list(poly.exterior.coords.xy[0])
    ys = list(poly.exterior.coords.xy[1])
    x_center = 0.5 * min(xs) + 0.5 * max(xs)
    y_center = 0.5 * min(ys) + 0.5 * max(ys)
    min_corner = Point(min(xs), min(ys))
    center = Point(x_center, y_center)
    shrink_distance = center.distance(min_corner) * factor

    if expand:
      poly_resized = poly.buffer(shrink_distance)  # expand
    else:
      poly_resized = poly.buffer(-shrink_distance)  # shrink
    return poly_resized
