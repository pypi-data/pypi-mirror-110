from shapely.geometry import Polygon, MultiPolygon  # type: ignore[import]

from geomesh.raster import Raster
from geomesh.mesh.base import BaseMesh
from geomesh.geom.base import BaseGeom
from geomesh.geom.raster import RasterGeom
from geomesh.geom.mesh import MeshGeom
from geomesh.geom.shapely import PolygonGeom, MultiPolygonGeom
from geomesh.geom.collector import GeomCollector


class Geom(BaseGeom):
    """
    Factory class that creates and returns correct object type
    based on the input type
    """

    def __new__(cls, geom, **kwargs):
        """
        Input parameters
        ----------------
        geom:
            Object to use as input to compute the output mesh hull.
        """

        if isinstance(geom, Raster):
            return RasterGeom(geom, **kwargs)

        elif isinstance(geom, BaseMesh):
            return MeshGeom(geom, **kwargs)

        elif isinstance(geom, Polygon):
            return PolygonGeom(geom, **kwargs)

        elif isinstance(geom, MultiPolygon):
            return MultiPolygonGeom(geom, **kwargs)

        elif isinstance(geom, (list, tuple)):
            return GeomCollector(geom, **kwargs)

        else:
            raise TypeError(
                f'Argument geom must be of type {BaseGeom} or a derived type, '
                f'not type {type(geom)}.')

    @staticmethod
    def is_valid_type(geom):
        return isinstance(geom, BaseGeom)

    def get_multipolygon(self, **kwargs) -> MultiPolygon:
        raise NotImplementedError
