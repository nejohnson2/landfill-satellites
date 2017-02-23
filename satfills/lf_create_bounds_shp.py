#!/usr/bin/env python
# Nicholas E. Johnson

'''
Read in a shapefile with point geometries.  Create 
a buffer around those geometries and export a new
shapefile.
'''

import os
import argparse
import rasterio
from shapely.geometry import Polygon
import geopandas as gp

parser = argparse.ArgumentParser()

def create_buffer(bounds, dist):
    '''
    Parameters
    ----------
    bounds : array,
      Minx, miny, maxx and maxy of geometry
    dist : float,
      Distance to create buffer
    '''
    n_minx = bounds['minx'] - dist
    n_miny = bounds['miny'] - dist
    n_maxx = bounds['maxx'] + dist
    n_maxy = bounds['maxy'] + dist
    
    coords = ((n_minx, n_miny), (n_minx, n_maxy), (n_maxx, n_maxy), (n_maxx, n_miny), (n_minx, n_miny))
    return Polygon(coords)
    
def km_to_deg(km):
    '''
    Parameters
    ----------
    km: float,
        Distance in km to be converted latlng
    '''
    return km * (1./110.574)


def main(inFile, distance):
    '''Increase bounds of point geometry
    Parameters:
    ----------
    inPath : string,
        Input point geometry shapefile. 
    dst : string,
        Ouput shapefile
    distance : int,
        Distance in km to be converted to 
        degree distance

    Returns:
    -----
    shapefile
    '''
    # read shapefile
    df = gp.read_file(inFile)

    # get existing bounds of all points
    bounds = df['geometry'].bounds
    
    # distance to increase
    dist = km_to_deg(distance)

    # create new geometry
    df['geometry'] = bounds.apply(create_buffer, axis=1, args=(dist,))


    dpath, fname = os.path.split(inFile)

    # create destination directory if doesnt exist
    outDir = os.path.join(dpath, fname[:-4] + '_Polygons')
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    # create outFile name
    fname = fname[:-4] + '_Polygons.shp'
    outFile = os.path.join(outDir, fname)

    df.to_file(outFile)


if __name__ == '__main__':
    parser.add_argument('--inPath', action='store', dest='inPath', required=True, 
        help='Input shapefile that contains point geometries.')    
    parser.add_argument('--distance', action='store', dest='distance', required=True, 
        help='Distance in km to be converted to degree distance')    

    args = parser.parse_args()

    main(args.inPath, int(args.distance))