#!/usr/bin/env python
'''ls_reproject.py 

Reproject landsat data to a common
reference system

Source:
https://mapbox.github.io/rasterio/topics/reproject.html

'''

import os
import argparse
import rasterio
import numpy as np
from rasterio.warp import calculate_default_transform, reproject, RESAMPLING

parser = argparse.ArgumentParser()

def reproject_geotiff(fpath, dst_crs):
	'''Reproject a geotiff into a new CRS 

	Parameters:
	----------
	fpath : string,
		Path to landsat geotiff image
	dst_crs : string,
		Coordinate reference system used for reprojection

	Returns:
	-------
	Creates a new .TIF file 
	'''

	dpath, fname = os.path.split(fpath)
	outFile = os.path.join(dpath, fname[:-4] + '-wgs84.TIF')

	with rasterio.open(fpath) as src:
		# calculate transformation
		affine, width, height = calculate_default_transform(
			src.crs, dst_crs, src.width, src.height, *src.bounds)

		data = src.read()
		kwargs = src.meta.copy()
		kwargs.update({
			'crs': dst_crs,
			'transform': affine,
			'affine': affine,
			'width': width,
			'height': height
		})

		# open file to write new projection
		with rasterio.open(outFile, 'w', **kwargs) as dst:
			for i, band in enumerate(data, 1):
				dest = np.zeros_like(band)

				reproject(
					source=band,
					destination=dest,
					src_transform=src.affine,
					src_crs=src.crs,
					dst_transform=affine,
					dst_crs=dst_crs,
					resampling=RESAMPLING.nearest)

			# write to opened file
			dst.write(dest, indexes=i)


if __name__ == '__main__':
    parser.add_argument('--fpath', action='store', dest='fpath', required=True, 
        help='Landsat image to be reprojected')    
    parser.add_argument('--crs', action='store', dest='crs', default='EPSG:4326', 
        help='Coordinate reference system used for reprojection')    

    args = parser.parse_args()

    reproject_geotiff(args.fpath, args.crs)