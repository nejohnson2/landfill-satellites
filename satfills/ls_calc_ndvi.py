import os
import argparse

parser = argparse.ArgumentParser()

def read_band(fpath):
	'''Read Landsat band

	Parameters:
	----------
	fpath : string,
		Path to .tiff band image

	Returns:
	-------
	band : ndarray
	'''
	with rasterio.open(fpath) as src:
		band = src.read(1)

	return band

def calc_ndvi(b3_path, b4_path):
	b3 = read_band(b3_path)
	b4 = read_band(b4_path)
	ndvi = (b4.astype(float) - b3.astype(float)) / (b4 + b3)
	return ndvi

if __name__ == '__main__':
    parser.add_argument('--b3', action='store', dest='b3_path', required=True, 
        help='Landsat Band 3 file')    
    parser.add_argument('--b4', action='store', dest='b4_path', required=True, 
        help='Landsat Band 4 file')    

    args = parser.parse_args()

    calc_ndvi(args.b3_path, args.b4_path)