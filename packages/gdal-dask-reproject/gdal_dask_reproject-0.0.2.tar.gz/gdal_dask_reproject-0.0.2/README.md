## GDAL Reprojection with Dask Arrays

#### Reprojection of maps with coordinate referrence systems (crs), using GDAL's implementation with Rasterio and supporting Dask backed arrays for parallel computing.    

#### Please note: this is not ready yet. It still has issues with missing data and needs to have support added for more features to be practical.
<br/>

```pip install gdal_dask_reproject```

```conda install -c chlochlo gdal_dask_reproject```
<br/>

#### Usage:
##### Import cc_reproject from the main module; then apply cc_reproject with arguments for the input DataArray (containing Rioxarray compatible crs attrs and coords) and the destination crs desired. 

```
from cc_reproject import cc_reproject

cc_reproject(xr.DataArray(np or dask), dst_crs)
```

#### Built with an eye to the work of Kirill Kouzoubov in OpenDataCube and with the desire to have a standalone GDAL dask reprojection package: (Note: all errors are my own).

[Issue in rioxarray](https://github.com/corteva/rioxarray/issues/119)

[ODC code](https://github.com/opendatacube/odc-tools/blob/develop/libs/algo/odc/algo/_warp.py)
