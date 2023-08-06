import logging

from jigsawpy import jigsaw_msh_t, jigsaw_jig_t
from jigsawpy import libsaw
import numpy as np
from pyproj import CRS
from typing import Union


from geomesh import utils
from geomesh.mesh import Mesh
from geomesh.hfun import Hfun
from geomesh.hfun.base import BaseHfun
from geomesh.geom import Geom
from geomesh.geom.base import BaseGeom

_logger = logging.getLogger(__name__)


class GeomDescriptor:

    def __set__(self, obj, val):
        if not isinstance(val, BaseGeom):
            raise TypeError(f'Argument geom must be of type {Geom}, '
                            f'not type {type(val)}.')
        obj.__dict__['geom'] = val

    def __get__(self, obj, val):
        return obj.__dict__['geom']


class HfunDescriptor:

    def __set__(self, obj, val):
        if not isinstance(val, BaseHfun):
            raise TypeError(f'Argument hfun must be of type {Hfun}, '
                            f'not type {type(val)}.')
        obj.__dict__['hfun'] = val

    def __get__(self, obj, val):
        return obj.__dict__['hfun']


class OptsDescriptor:

    def __get__(self, obj, val):
        opts = obj.__dict__.get('opts')
        if opts is None:
            opts = jigsaw_jig_t()
            opts.mesh_dims = +2
            opts.optm_tria = True
            opts.hfun_scal = 'absolute'
            obj.__dict__['opts'] = opts
        return opts


class JigsawDriver:

    _geom = GeomDescriptor()
    _hfun = HfunDescriptor()
    _opts = OptsDescriptor()

    def __init__(
            self,
            geom: Geom,
            hfun: Hfun,
            initial_mesh: bool = False,
            crs: Union[str, CRS] = None,
            verbosity: int = 0,
    ):
        """
        geom can be SizeFunction or PlanarStraightLineGraph instance.
        """
        self._geom = geom
        self._hfun = hfun
        self._init = initial_mesh
        self._crs = CRS.from_user_input(crs) if crs is not None else crs
        self._opts.verbosity = verbosity

    def run(self, sieve=None):

        hfun_msh_t = self.hfun.msh_t()

        output_mesh = jigsaw_msh_t()
        output_mesh.mshID = 'euclidean-mesh'
        output_mesh.ndims = 2
        output_mesh.crs = hfun_msh_t.crs

        self.opts.hfun_hmin = np.min(hfun_msh_t.value)
        self.opts.hfun_hmax = np.max(hfun_msh_t.value)

        geom_msh_t = self.geom.msh_t()

        _logger.info('Calling libsaw.jigsaw() ...')
        libsaw.jigsaw(
            self.opts,
            geom_msh_t,
            output_mesh,
            init=hfun_msh_t if self._init is True else None,
            hfun=hfun_msh_t
        )

        # post process
        if output_mesh.tria3['index'].shape[0] == 0:
            _err = 'ERROR: Jigsaw returned empty mesh.'
            _logger.error(_err)
            raise Exception(_err)

        if self._crs is not None:
            utils.reproject(output_mesh, self._crs)

        _logger.info('Finalizing mesh...')
        if self.opts.hfun_hmin > 0:
            output_mesh = utils.remesh_small_elements(
                self.opts, geom_msh_t, output_mesh, hfun_msh_t)
        utils.finalize_mesh(output_mesh, sieve)

        _logger.info('done!')
        return Mesh(output_mesh)
