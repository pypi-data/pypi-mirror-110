## GDAL Reprojection with Dask Arrays

#### Reprojection of maps with coordinate referrence systems (crs), using GDAL's implementation with Rasterio and supporting Dask backed arrays for parallel computing.  
##### Options for setting chunks or number of blocks in each dimension for easy dask chunking. 

#### Also provides the 'geo' accessor for DataArrays
<br/>

```pip install gdal_dask_reproject```

```conda install -c chlochlo gdal_dask_reproject```
<br/>

#### Usage:
##### Import reproject from cc_reproject; then apply reproject with arguments for the input DataArray (containing Rioxarray compatible crs attrs and coords) and the destination crs desired.

##### If the input is a dask-backed data array then chunking is done automatically for the destination, matching the chunk structure of the input.

##### If the input is a np backed data array then the default will run a single reproject and return a np backed data array. But, setting the destination chunks or numblocks will return a dask backed array. 
###### Note: the chunks input refers to the destination chunks; if this is provided without dst_shape, it will determine the dst_shape; if chunks and dst_shape are provided, the chunks in each dimension must sum to the provided shape.

###### Note on providing chunks when using an input that is already chunked: band chunking must match from src to dst; i.e. if the src band chunks are (1, 2) the destination must also have them in that order. If not, reproject will coerce the dst to match the src band chunking.
###### Note on using numblocks for chunking: numblocks is currently set to chunk the dst array by a math.ceil operation, so chunking an uneven dimension, like 3 bands for example, returns chunks (2, 1). 

##### Kwargs are also available for passing through to rasterio.warp.reproject. For example, setting resampling. See below.

##### Example:

```
from cc_reproject import reproject

src = xarray.DataArray(np or dask array)
src_crs --> 'EPSG:4326'  # set in spatial_ref coords according to rioxarray compatibility
dst_crs = 'EPSG:3857'

reproject(src, dst_crs, **kwargs)

--> xarray.DataArray(np or dask)
```

```
reproject(xarray.DataArray(np), dst_crs, numblocks=(1, 2, 2), **kwargs)
--> xarray.DataArray(dask) chunked 1, 2, 2 times along the band, height, and width dimensions
```
##### Using the 'geo' accessor:

```
from cc_reproject import geo

my_data_array = xarray.DataArray(...)
my_data_array.geo.reproject(dst_crs, **kwargs)
--> reprojected xarray.DataArray
```
##### Adding kwargs for rasterio.warp.reproject
```
from cc_reproject import reproject
from rasterio.warp import Resampling

my_data_arr = xarray.DataArray(np or dask)
reproject(my_data_arr, dst_crs, resampling=Resampling.min)
--> reprojected xarray.DataArray(np or dask) resampled according to input
```
##### Support for multiband chunking
gdal_dask_reproject also allows chunking along band dimension for multiband rasters. You can add `band_kwargs` to apply specifically to each band chunk.
`band_kwargs` is a dict with keys for each band chunk index, and values that are dicts of kwargs for each band index; for example: if 3 bands are split into 2 chunks 1, 2 in length, then keys would be `0` and `1`.
You can also set global kwargs differing from the ones set for specific band chunks. Any band_kwargs will overrride global kwargs for those bands specified, but the rest of the kwargs and the bands not included in band_kwargs will have the global settings.
```
from cc_reproject import reproject
from rasterio.warp import Resampling

# 3-band raster, for example
my_data_arr = xarray.DataArray(np or dask: shape = (3, 200, 400))
band_chunks = (1, 2)
band_kwargs = {
    0: {
        'resampling': Resampling.min
    },
}

# 300 and 600 tuples below are arbitrary chunk height and width settings. Using these, the returned DataArray will
# have the shape (3, 300, 600), based on summing the chunks specified for the destination.
reproject(my_data_arr, dst_crs, chunks=(band_chunks, (300,), (600,)), band_kwargs=band_kwargs, resampling=Resampling.bilinear)
--> xarray.DataArray(dask) 
    band chunk 0: band 1: resampled by min
    band chunk 1: band 2 and band 3: resampled by bilinear
```

#### Based on the work of Kirill Kouzoubov in OpenDataCube and with the desire to have a standalone GDAL dask reprojection package: (Note: all errors are my own).

[Issue in rioxarray](https://github.com/corteva/rioxarray/issues/119)

[ODC code](https://github.com/opendatacube/odc-tools/blob/develop/libs/algo/odc/algo/_warp.py)
