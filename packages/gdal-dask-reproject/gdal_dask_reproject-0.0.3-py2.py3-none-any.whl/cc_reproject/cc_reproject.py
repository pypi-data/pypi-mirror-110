from dask.array.routines import isin
from xrspatial.utils import ArrayTypeFunctionMapping
import numpy as np
import xarray as xr
from dask.highlevelgraph import HighLevelGraph
import dask.array as da

from pyproj import Transformer
import rioxarray  # noqa: F401
import rasterio
from rasterio.warp import reproject

import math


class ArrayFuncMap:

    def __init__(self, np_func, dask_func):
        self.np_func = np_func
        self.dask_func = dask_func

    def __call__(self, arr):
        if isinstance(arr.data, np.ndarray):
            return self.np_func
        if isinstance(arr.data, da.Array):
            return self.dask_func
        else: raise NotImplementedError('only np and dask arrays supported for now')



def tokenize(prefix):
    return "{}-{:08x}".format(prefix,
                              np.random.randint(0, 0xFFFFFFFF))


def _chunkshapes(chunks):
    chunkshapes = []
    for i in range(len(chunks[0])):
        for j in range(len(chunks[1])):
            for k in range(len(chunks[2])):
                chunkshapes.append((chunks[0][i], chunks[1][j], chunks[2][k]))
    return chunkshapes


def _chunklocs(numblocks):
    chunklocs = []
    for i in range(numblocks[0]):
        for j in range(numblocks[1]):
            for k in range(numblocks[2]):
                chunklocs.append((i, j, k))
    return chunklocs


def _arr_locs(chunklocs, chunkshapes):
    locs_shapes = dict(zip(chunklocs, chunkshapes))
    arr_locs = []
    for i in range(len(chunkshapes)):
        arr_locs.append([])
        for j in range(3):
            start_pos = 0
            dim_position = chunklocs[i][j]
            if dim_position > 0:
                prev_len = 0
                for num in range(dim_position):
                    itera = [0, 0, 0]
                    itera[j] = num
                    itera = tuple(itera)
                    prev_shape = locs_shapes[itera]
                    prev_shape_dim_len = prev_shape[j]
                    prev_len += prev_shape_dim_len
                start_pos += prev_len
            end_pos = start_pos + chunkshapes[i][j]
            arr_locs[i].append((start_pos, end_pos))
    return arr_locs


def _chunk_bounds(src_shape, res, offsets, arr_locs):
    src_b, src_height, src_width = src_shape
    resx, resy = res
    resy = -resy
    xoff, yoff = offsets
    chunk_bounds = []
    for locs in arr_locs:
        arr_left, arr_right = locs[2]
        arr_bottom, arr_top = locs[1]
        ch_bottom = src_height - arr_top
        ch_top = src_height - arr_bottom
        left, right = arr_left * resx + xoff, arr_right * resx + xoff
        bottom, top = ch_bottom * resy + yoff, ch_top * resy + yoff
        ch_bounds = left, bottom, right, top
        chunk_bounds.append(ch_bounds)
    return chunk_bounds


def _transform_bounds(bounds, src_crs, dst_crs):
    transformer = Transformer.from_crs(src_crs, dst_crs, always_xy=True)
    left, bottom, right, top = bounds
    dst_lb = transformer.transform(left, bottom)
    dst_rt = transformer.transform(right, top)
    dst_bounds = *dst_lb, *dst_rt
    return dst_bounds


def _chunks_from_shapes_numblocks(chunkshapes, numblocks):
    np_arr = np.asarray(chunkshapes).reshape(*numblocks, 3)
    first_col = np_arr[:,:,0,:]
    hs = first_col[:,:,1].tolist()[0]
    hs = tuple(hs)
    first_row = np_arr[:,0,:,:]
    ws = first_row[:,:,2].tolist()[0]
    ws = tuple(ws)
    bands_dim = np_arr[0,:,:,:]
    bs = bands_dim[:,:,0].flatten()
    if np.all(bs == 1):
        bs = (1,)
    else:
        raise NotImplementedError('multiband chunking not implemented')
    chunks = (bs, hs, ws)
    return chunks


def _calc_reproject_shape(src_bounds, dst_bounds, src_shape):
    s_left, s_bottom, s_right, s_top = src_bounds
    s_b, s_height, s_width = src_shape
    src_X = s_right - s_left
    src_Y = s_top - s_bottom
    src_XperY = src_X / src_Y
    
    d_left, d_bottom, d_right, d_top = dst_bounds
    dst_X = d_right - d_left
    dst_Y = d_top - d_bottom
    dst_XperY = dst_X / dst_Y

    d_width, d_height = abs(int(math.ceil(s_width * (dst_XperY / src_XperY)))),\
        abs(int(math.ceil(s_height * (src_XperY / dst_XperY))))
    dst_shape = [s_b, d_height, d_width]
    return dst_shape


def _correct_dbk_shapes(dbk_shapes, numblocks):
    np_arr = np.asarray(dbk_shapes)
    orig_shape = np_arr.shape
    np_arr = np_arr.reshape(*numblocks, 3)
    for i in range(numblocks[2]):
        cols = np_arr[:,:,i,:]
        ws = cols[:,:,2]
        mean_w = ws.mean()
        ws[:,:] = mean_w
    for i in range(numblocks[1]):
        rows = np_arr[:,i,:,:]
        hs = rows[:,:,1]
        mean_h = hs.mean()
        hs[:,:] = mean_h
    dbk_shapes = np_arr.reshape(orig_shape).tolist()
    return dbk_shapes


def _sum_dbk_shapes(chunkshapes, numblocks):
    np_arr = np.asarray(chunkshapes).reshape(*numblocks, 3)
    first_col = np_arr[:,:,0,:]
    tot_height = first_col[:,:,1].sum()
    first_row = np_arr[:,0,:,:]
    tot_width = first_row[:,:,2].sum()
    dst_hw = (tot_height, tot_width)
    return dst_hw


def _add_xr_da_coords(data, bounds):
    bands, height, width = shape = data.shape
    left, bottom, right, top = bounds
    resx, resy = (right - left) / width, (top - bottom) / -height
    xs = np.arange(width) * resx + (left + resx / 2)
    ys = np.arange(height) * resy + (bottom + resy / 2)
    xs_da = xr.DataArray(xs, dims=('x'))
    ys_da = xr.DataArray(ys, dims=('y'))
    bands = np.arange(1, bands + 1, dtype=np.int64)
    bands_da = xr.DataArray(bands, dims=('band'))
    data_da = xr.DataArray(data, dims=('band', 'y', 'x'))
    data_da.coords['x'] = xs_da
    data_da.coords['y'] = ys_da
    data_da.coords['band'] = bands_da
    return data_da


def _block_reproject(block, sbk_bounds, dbk_bounds, dbk_shape, src_crs, dst_crs):
    sbk_bands, sbk_height, sbk_width = sbk_shape = block.shape
    s_left, s_bottom, s_right, s_top = sbk_bounds
    src_resx, src_resy = (s_right - s_left) / sbk_width, (s_top - s_bottom) / -sbk_height
    
    sbk_transform = rasterio.Affine(src_resx, 0, s_left, 0, src_resy, s_top)
    
    d_left, d_bottom, d_right, d_top = dbk_bounds
    dbk_b, dbk_height, dbk_width = dbk_shape
    dst_resx, dst_resy = dst_res = (d_right - d_left) / dbk_width, (d_top - d_bottom) / -dbk_height
    
    dbk_transform = rasterio.Affine(dst_resx, 0, d_left, 0, dst_resy, d_top)
    
    src_nodata = dst_nodata = 0
    
    source = block
    destination = np.zeros((1, dbk_height, dbk_width), dtype=np.uint8)
    
    reproject(source,
              destination=destination,
              src_transform=sbk_transform,
              src_crs=src_crs,
              src_nodata=src_nodata,
              dst_transform=dbk_transform,
              dst_crs=dst_crs,
              dst_nodata=dst_nodata)
    
    return destination


def _numpy_reproject(arr, dst_crs, **kwargs):
    data = arr.data
    src_crs = arr.rio.crs
    src_shape = data.shape
    src_bounds = arr.rio.bounds()
    dst_bounds = _transform_bounds(src_bounds, src_crs, dst_crs)
    dst_shape = _calc_reproject_shape(src_bounds, dst_bounds, src_shape)
    
    reprojected_data = _block_reproject(data, src_bounds, dst_bounds, dst_shape, src_crs, dst_crs)
    reprojected_da = _add_xr_da_coords(reprojected_data, dst_bounds)
    return reprojected_da


def _dask_reproject(arr, dst_crs, **kwargs):
    # TODO: Add test for crs area of use
    src_bands, src_height, src_width = src_shape = arr.data.shape
    src_bounds = arr.rio.bounds()
    src_crs = arr.rio.crs
    dst_bounds = _transform_bounds(src_bounds, src_crs, dst_crs)
    src_res = arr.rio.resolution()
    src_offsets = (src_bounds[0], src_bounds[1])
    numblocks = arr.data.numblocks
    chunks = arr.data.chunks
    chunklocs = _chunklocs(numblocks)
    chunkshapes = _chunkshapes(chunks)
    arr_locs = _arr_locs(chunklocs, chunkshapes)
    sbk_bounds = _chunk_bounds(src_shape, src_res, src_offsets, arr_locs)
    dbk_bounds = [_transform_bounds(bounds, src_crs, dst_crs) for bounds in sbk_bounds]
    
    sd_bounds_s_shp = list(zip(sbk_bounds, dbk_bounds, chunkshapes))
    dbk_shapes = [_calc_reproject_shape(s_bounds, d_bounds, s_shape)
                  for s_bounds, d_bounds, s_shape in sd_bounds_s_shp]
    dbk_shapes = _correct_dbk_shapes(dbk_shapes, numblocks)
    dst_chunks = _chunks_from_shapes_numblocks(dbk_shapes, numblocks)
    dst_hw = _sum_dbk_shapes(dbk_shapes, numblocks)
    dst_shape = (src_bands, dst_hw[0], dst_hw[1])
    loc_bounds_dst_shp = dict(zip(chunklocs, list(zip(sbk_bounds, dbk_bounds, dbk_shapes))))    

    # Now, the fun part!!!
    def apply_reproject(self, loc_bounds_dst_shp, src_crs, dst_crs):
        layer = {}
        name = tokenize('reproject')
        for key in self.__dask_keys__():
            for item in key:
                for sub_item in item:
                    input_key, i, j, k = sub_item
                    loc = (i, j, k)
                    sbk_bounds, dbk_bounds, dbk_shape = loc_bounds_dst_shp[loc]
                    layer[(name, i, j, k)] = (_block_reproject,
                                              (input_key, i, j, k),
                                              sbk_bounds,
                                              dbk_bounds,
                                              dbk_shape,
                                              src_crs,
                                              dst_crs)
        graph = HighLevelGraph.from_collections(name, layer, dependencies=[self])
        return da.Array(graph, name, chunks=dst_chunks, dtype=np.uint8, shape=dst_shape)
    reprojected_data = apply_reproject(arr.data, loc_bounds_dst_shp, src_crs, dst_crs)
    reprojected_da = _add_xr_da_coords(reprojected_data, dst_bounds)
    return reprojected_da


def cc_reproject(arr, dst_crs, **kwargs):
    mapper = ArrayFuncMap(np_func=_numpy_reproject,
                          dask_func=_dask_reproject)
    reprojected = mapper(arr)(arr, dst_crs, **kwargs)
    return reprojected