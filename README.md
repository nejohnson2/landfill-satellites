# landfill-satellites

## Source Data
### Landfills
There are four categories of landfill data in New York State.  Three are derived from the New York State Department of Environmental Conservation and one was taken from somewhere else.  The source of this information is from an [ArcGIS map](http://www.arcgis.com/home/item.html?id=acb6d6a9eca04ac9b3e25b397bc0560b). 

1. **Construction and Demolition Debris Landfills in New York State**

   Data were digitized from information supplied by the New York State Department of Environmental Conservation's Division of Materials Management/Solid Waste Management Facilities. Coordinates in UTM, Zone 18. Current as of 12/30/2011. [http://www.dec.ny.gov/docs/materials_minerals_pdf/cdlist.pdf](http://www.dec.ny.gov/docs/materials_minerals_pdf/cdlist.pdf)

2. **Industrial and Commercial Waste Landfills in New York State**

   Data were digitized from information supplied by the New York State Department of Environmental Conservation's Division of Materials Management/Solid Waste Management Facilities. Coordinates in UTM, Zone 18. Current as of 12/30/2011. [http://www.dec.ny.gov/docs/materials_minerals_pdf/indlist.pdf](http://www.dec.ny.gov/docs/materials_minerals_pdf/indlist.pdf)

3. **Privately-owned Landfills in New York State**

   This dataset shows locations of privately owned landfills in New York State. Information was gathered from [http://www.manta.com/mb_45_E33B908E_33/sanitary_landfill_operation/new_york](http://www.manta.com/mb_45_E33B908E_33/sanitary_landfill_operation/new_york) and addresses were entered into Google Maps to determine latitude and longitude coordinates, adjusted after visual inspection of aerial basemaps.  

4. **Active Municipal Solid Waste Landfills in New York State**

   Data were digitized from information supplied by the New York State Department of Environmental Conservation's Division of Materials Management/Solid Waste Management Facilities. [http://www.dec.ny.gov/docs/materials_minerals_pdf/mswlist.pdf](http://www.dec.ny.gov/docs/materials_minerals_pdf/mswlist.pdf)

5. **New Jersey Landfills**

   [This map](http://njogis-newjersey.opendata.arcgis.com/datasets/05b964b785d2417ca5256077c943b818_5) was created to provide accurate spatial information regarding solid waste landfills in New Jersey [greater than 35 acres]. The points delineated in this data were originally taken from original paper topoquads marked by field personnel, and location data developed by the Site Remediation Program. These delineations were later refined using site plans, tax parcel data and aerial photography by employees of the Solid and Hazardous Waste Program.  [Direct Metadata Link](https://njgin.state.nj.us/NJ_NJGINExplorer/ShowMetadata.jsp?docId=31463B9F-9F74-4E33-B22D-8B0971580AE1)

6. **Active Landfills in Connecticut ***
   
   This list was compiled on ```Feb 16, 2017``` and taken from the [Connecticut Department of Energy and Environment](http://www.ct.gov/deep/cwp/view.asp?a=2718&depNav_GID=1646&q=325462).  Does not contain spaitial information.

### Satellite Images
For the project I will be using data from the **Landsat 8** satellite which collects data in the thermal infrared spectrum.  The data can be found on [Glovis](http://glovis.usgs.gov) (does not work on Chrome).  New York City is located in Path/Row ```13/32``` and ```14/32```. 

---

### Workflow
```landsat-util``` is a great tool for getting and performing basic manipulations on Landsat 8 data.  Install:

```
sudo pip install landsat-util
```

Then you can search for scense by lat/lon or path/row and download scenes. During download you can 1) specify which bands are needed and 2) provide clipping information.  As an example:

```
landsat search -p 013,032
```

## Resources
- [Putting Landsat 8's bands to work](https://www.mapbox.com/blog/putting-landsat-8-bands-to-work/)

