#!/usr/bin/env python
'''ls_download.py 

Automate download of landsat data using specific
source locations.  This is a wrapper for the
landsat-util module.

by Nicholas E. Johnson
'''
import json, os
import subprocess
import argparse
import pandas as pd 

parser = argparse.ArgumentParser()

def download_data(sceneID, dpath, clip=None):
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

	return subprocess.call(command)

def get_sceneID(latlng, clouds):
	'''Run landsat search utility to extract sceneID from lat/lng

	Parameters
	----------
	latlng : list,
		Latitude and longitude coordinates

	clouds : int,
		Maximum percentage of cloud cover allowed.  Default is 10.

	Returns
	-------
	sceneID : string,
		Example: LC81660392014196LGN00

	'''

	search = ['--lat', '--lon']
	search.insert(1, str(latlng[0]))
	search.insert(3, str(latlng[1]))

	command = ['landsat', 'search', '--json', '--cloud', str(clouds), "--end", "january 01 2015"]
	command.extend(search)
	
	output = subprocess.check_output(command)
	
	results = json.loads(output)
	print "Found {} images".format(results['total_returned'])

	return results['results'][0]['sceneID']


def unzip():
	'''Unzip any .tar.gz files in a directory'''
	return

def create_mask():
	'''Clip Landsat image with landfill bounds'''
	with rasterio.open("tests/data/RGB.byte.tif") as src:
		out_image, out_transform = rasterio.tools.mask.mask(src, features,
														crop=True)
		out_meta = src.meta.copy()

if __name__ == '__main__':
	parser.add_argument('--outPath', action='store', dest='outPath', required=True, 
		help='Output file path')    
	parser.add_argument('--clouds', action='store', dest='clouds', default=10, 
		help='Amount of acceptable cloud cover')    

	args = parser.parse_args()

	fname = '../data/output/landfills_master.csv'
	data = pd.read_csv(fname)

	for coords in data[['lat','lng']].values:
		
		sceneID = get_sceneID(latlng=coords, clouds=args.clouds)

		download_data(sceneID=str(sceneID), dpath=args.outPath)
		break
	
