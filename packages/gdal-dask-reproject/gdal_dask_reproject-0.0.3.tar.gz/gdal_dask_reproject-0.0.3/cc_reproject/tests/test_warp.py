from cc_reproject.warp import reproject
import rioxarray


dst_crs = 'EPSG:3857'
elev_ll = rioxarray.open_rasterio('../../../../elev_rgb2.tif')
reprojected_np = reproject(elev_ll, dst_crs)

elev_ll_dsk = elev_ll.chunk(((3,), (120, 120), ()))
