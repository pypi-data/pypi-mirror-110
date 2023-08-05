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

reproject(xr.DataArray(np or dask), dst_crs, **kwargs)

--> xr.DataArray(np or dask)
```

```
reproject(xr.DataArray(np), dst_crs, numblocks=(1, 2, 2), **kwargs)
--> xr.DataArray(dask) chunked 1, 2, 2 time along band, height, width
```
##### Using the 'geo' accessor:

```
from cc_reproject import geo

my_data_array = xr.DataArray(...)
my_data_array.geo.reproject(dst_crs, **kwargs)
--> reprojected xr.DataArray
```

#### Inspired by the work of Kirill Kouzoubov in OpenDataCube and with the desire to have a standalone GDAL dask reprojection package: (Note: all errors are my own).

[Issue in rioxarray](https://github.com/corteva/rioxarray/issues/119)

[ODC code](https://github.com/opendatacube/odc-tools/blob/develop/libs/algo/odc/algo/_warp.py)
