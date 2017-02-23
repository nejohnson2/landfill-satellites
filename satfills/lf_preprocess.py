#!/usr/bin/env python
# Nicholas E. Johnson

'''
Create a master csv with columns:

	lat,lon,waste_type,name,desc

Processes include:

0. Geoencode CT landfills
1. Extract coordinates from spatial data
2. Create coordinates if necessary (geoencode)
3. Standardize and merge data 
'''
import os
import pandas as pd 
import geopandas as gp 
from shapely.geometry import Point

# --
# Geoencode landfill data from CT
# --
def geoencode(address):
	'''Get lat/long from Google API

	Parameters:
	----------
	address: string,
		The address to lookup (ex. 30-27 Greenpoint Avenue LIC, NY)
	'''
	landfill = " ".join([address['Facility Address'], address['Town'], ', ', address['State']])

	g = geocoder.google(landfill)
	
	if g.confidence >= 7:
		return pd.Series({'lat':g.lat, 'lng':g.lng})
	else:
		return pd.Series({'lat': None, 'lng': None})

def geoencode_CT_landfills():
	df = pd.read_csv('data/Connecticut_Active_Landfills.csv')
	df['State'] = 'CT'
	data = pd.concat([df,df.apply(geoencode, axis=1)], axis=1)
	data.to_csv('data/Connecticut_Active_Landfills.csv', index=False)

# --
# Utilities
# --
def create_point_geometry(x):
	'''
	Create geopandas geometry from lat/lng 
	columns in a Dataframe

	Parameters
	----------
	latlng: Dataframe,
		Two columns with lat and lon coordinates
	'''
	return Point(x['lng'], x['lat'])

def df_to_spatial(df, crs={'init':'epsg:4326'}):
	'''Turn dataframe into spaital data

	Parameters
	----------
	df : pandas.Dataframe,
		Dataframe with lat/lng columns

	crs : dict,
		Projection to use.  Default is WG84

	Returns
	-------
	geopandas.GeoDataframe 
	'''
	df['geometry'] = df.apply(create_point_geometry, axis=1)
	df = gp.GeoDataFrame(df)
	df.crs = crs
	return df

def get_latlng(fpath):
	'''Extract lat/lng into columns from
	spatial data'''

	fname = os.path.split(fpath)[1]
	
	# if it's not spatial data, make it so
	if fpath[-3:] == 'csv':
		lf = pd.read_csv(fpath)
		lf = df_to_spatial(lf)
		lf = lf.dropna(subset=['lat','lng'])
		fname = fname[:-3] + 'shp'
	else:
		lf = gp.read_file(fpath)  
		lf = lf.to_crs({'init':'epsg:4326'})
		
		if 'lat' not in lf.columns or 'lng' not in lf.columns:
			lf['lng'] = lf['geometry'].map(lambda point: point.x)
			lf['lat'] = lf['geometry'].map(lambda point: point.y)
		
	fout = os.path.join('data/output', fname)
	cols = [col.lower() for col in lf.columns]
	lf.columns = cols
	lf.to_file(fout)


if __name__ == '__main__':
	fpath = ['construction_demo_debris_NYS/construction_demo_debris.shp',
			 'active_msw_landfills_NYS/active_msw_landfills.shp',
			 'industrial_commercial_NYS/industrial_commercial.shp',
			 'Landfill_Sites_in_New_Jersey/Landfill_Sites_in_New_Jersey.shp', 
			 'privately_owned_landfills_NYS/privately_owned_landfills_NYS.shp',
			 'Connecticut_Active_Landfills.csv']

	for i in fpath:
		get_latlng(os.path.join('data/',i)) 	

	# --
	# Standardize datasets
	# --
	data = []

	for i in glob.glob('data/output/*.shp'):
		f = gp.read_file(i)
		data.append(f)

	# Clean and Standardize
	d0 = data[0][['lat','lng','waste_type','name']]
	d1 = data[1][['lat','lng','waste type','owner']]
	d2 = data[2][['lat','lng','waste_type','company']]
	d3 = data[3][['lat','lng','waste_type','company']]
	d4 = data[4][['lat','lng','lfname']]
	d5 = data[5][['lat','lng','name']]

	d1 = d1.rename(columns={'waste type': 'waste_type', 'owner':'name'})

	d2 = d2.rename(columns={'company':'name'})
	d3 = d3.rename(columns={'company':'name'})

	d4 = d4.rename(columns={'lfname':'name'})

	d4['waste_type'] = 'unknown'
	d5['waste_type'] = 'unknown'

	d0['desc'] = 'NY msw'
	d1['desc'] = 'CT'
	d2['desc'] = 'NY construction'
	d3['desc'] = 'NY industrial/commercial'
	d4['desc'] = 'NJ'
	d5['desc'] = 'NY private'

	pd.concat([d0,d1,d2,d3,d4,d5], ignore_index=True).to_csv('data/output/landfills_master.csv', index=False)