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

##### If the input is a np backed data array then the default will run a single reproject and return a np backed data array. But, setting output chunks or numblocks will return a dask backed array. 

##### Kwargs are also available for passing through to rasterio.warp.reproject. For example, setting resampling. See below.

##### Example:

```
from cc_reproject import reproject

reproject(xarray.DataArray(np or dask), dst_crs, **kwargs)

--> xarray.DataArray(np or dask)
```

```
reproject(xarray.DataArray(np), dst_crs, numblocks=(1, 2, 2), **kwargs)
--> xarray.DataArray(dask) chunked 1, 2, 2 time along band, height, width
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
`band_kwargs` is a dict with keys for each band chunk index; for example: if 3 bands are split into 2 chunks 1, 2 in length, then keys would be `0` and `1`.
You can also set global kwargs differing from the ones set for specific band chunks and these will apply to all other bands.
```
from cc_reproject import reproject
from rasterio.warp import Resampling

# 3-band raster, for example
my_data_arr = xarray.DataArray(np or dask: shape = (3, 200, 400))
band_kwargs = {
    0: {
        resampling: Resampling.min
    },
}
reproject(my_data_arr, dst_crs, chunks=((1,1,1), (200,), (400,)), band_kwargs=band_kwargs, resampling=Resampling.bilinear)
--> xarray.DataArray(dask) 
    band 1: resampled by min
    band 2 and band 3: resampled by bilinear
```

#### Based on the work of Kirill Kouzoubov in OpenDataCube and with the desire to have a standalone GDAL dask reprojection package: (Note: all errors are my own).

[Issue in rioxarray](https://github.com/corteva/rioxarray/issues/119)

[ODC code](https://github.com/opendatacube/odc-tools/blob/develop/libs/algo/odc/algo/_warp.py)
