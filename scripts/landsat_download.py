import json
import subprocess
import pandas as pd 

def read_lat_lon(row):

	lat = str(row['lat'])
	lng = str(row['lng'])
	
	output = subprocess.check_output(['landsat', 'search', '--lat', lat, '--lon', lng, '--latest', str(10), '--json'])
	o = json.loads(output)
	
	print set([(i['path'], i['row']) for i in  o['results']])

	# stdout_value = proc.communicate()[0]
	# print '\tstdout:', repr(stdout_value)

def main():
	fname = '../data/output/landfills_master.csv'
	data = pd.read_csv(fname)

	data.head().apply(read_lat_lon, axis=1)

if __name__ == '__main__':
	main()