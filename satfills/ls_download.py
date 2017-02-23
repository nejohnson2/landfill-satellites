#!/usr/bin/env python
'''ls_download.py 

Automate download of landsat data using specific
source locations.  This is a wrapper for the
landsat-util module.

by Nicholas E. Johnson
'''
import json, os
import subprocess
import pandas as pd 

def download_data(sceneID, clip=None, dpath='./download/'):
	'''Run landsat download utility

	Parameters
	----------
	sceneID : string or list,
		Example: LC81660392014196LGN00

	clip : array,
		Values must be in WGS84 datum, and with longitude and latitude 
		units of decimal degrees separated by comma.
		Example: --clip=-346.06658935546875,49.93531194616915,-345.4595947265625,50.2682767372753

	dpath : string
		File path to save downloaded .tar.gz files
	'''
	
	if not os.path.exists(dpath):
    	os.makedirs(dpath)

	command = ['landsat', 'download', '-d', dpath]

	if type(sceneID) == str:
		command.append(sceneID)
	else:
		command.extend(sceneID)	

	subprocess.call(command)
	return

def get_sceneID(pathrow=None, latlng=None, clouds=10):
	'''Run landsat search utility to extract sceneID

	Parameters
	----------
	pathrow : str,
		Paths and Rows in order separated by comma. Use quotes "001,003".
        Example: path,row,path,row 001,001,190,204

    latlng : list,
    	Latitude and longitude coordinates

    clouds : int,
    	Maximum percentage of cloud cover allowed.  Default is 10.

    Returns
    -------
    sceneID : string,
    	Example: LC81660392014196LGN00

	'''
	try:
		if pathrow != None:
			search = ['-p ']
			search.insert(1, pathrow)
		elif latlng != None:
			search = ['--lat', '--lon']
			search.insert(1, str(latlng[0]))
			search.insert(3, str(latlng[1]))
		else:
			raise Exception('No input')
	except Exception as e:
		print e
		return

	command = ['landsat', 'search', '--geojson', '--cloud', str(clouds), '--latest', str(10)]
	command.extend(search)
	
	output = subprocess.check_output(command)
	results = json.loads(output)
	print results['results'][0]
	
	return 

def unzip():
	'''Unzip any .tar.gz files in a directory'''
	return

def create_mask():
	'''Clip Landsat image with landfill bounds'''
	with rasterio.open("tests/data/RGB.byte.tif") as src:
		out_image, out_transform = rasterio.tools.mask.mask(src, features,
	                                                    crop=True)
		out_meta = src.meta.copy()

def main():
	fname = '../data/output/landfills_master.csv'
	data = pd.read_csv(fname)

	for coords in data[['lat','lng']].values:
		sceneID = get_sceneID(latlng=coords)

	#clip = data['clip']
	
		download_data(sceneID=scene, clip=clip)
	
