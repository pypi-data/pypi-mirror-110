
## Quickstart

## About Heliware

Heliware is a Web-GL Powered Geo-Spatial Analytics Platform for developer ,analytics & data Scientist that provides GIS, Web Mapping, and spatial data science tools which help companies to get InSite in just few click using AI, Data Science & Advance Geo-Processing

## Contact 
For any query please contact rajan@heliware.co.in

### Description About heligeo module
heligeo module provides you high level geoprocessing and routing services 
---

* `routes`
* `isochrone`
* `polygon_union`
* `polygon_intersection`
* `alias_multistring`
* `point_buffer`
* `line_buffer`
* `point_within_polygon`

***

### How to get Api Key
[Visit Website](https://heliware.co.in/) to Access the ApiKey

### Requirements
`heligeo-py` is tested over `Python>=3.0`

## Installation
To install from PyPI, simply use pip:
```pip install heligeo```

## How to use
Most of the cases heligeo module accept `Polygon`,`Point`,`Lisestring` data that format must be `geojson`.

## Usage

### Basic Example Of Routing Service 
By default heligeo support four type of transport mode 
* `drive`
* `walk`
* `bike`
* `cycling`

#### Output format 
Output always `Geojson` response
#### Isochrone Service
``` 
from heligeo import heliRouteService
apikey = ''
longtitude = [88.3639]
latitude = [22.5726]
transport_mode = "drive" 
isochrone_data = heliRouteService.isochrone(apikey,latitude,longtitude,transport_mode)
```
#### Routing Service
```
apikey = ''
transport_mode = "drive" 
direction_coordinates = [[88.3639,22.5726],[72.8777,19.0760]] ### user can use multiple points
route_data = heliRouteService.route(apikey,direction_coordinates,transport_mode)

```

### Basic Example Of Geoprocessing Service 
* `heliGeoprocessingService.Union()`,`heliGeoprocessingService.Intersection()` function  accept multiple polygon data inside a list.
* In this example we shown only 2 polygon data 


#### Polygon Union Example
```
from heligeo import heliGeoprocessingService
apikey = ''
polygon1 = {"type": "FeatureCollection","features":[{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[77.4029103817493, 28.36918941103731, 0.0], [77.40184896262588, 28.3722403721131, 0.0][77.39922678901301, 28.37081966588294, 0.0], [77.40030856003351, 28.36816909494472, 0.0], [74029103817493, 28.36918941103731, 0.0]]]
  }}]}
polygon2 = {"type": "FeatureCollection","features":[{
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[77.40486731638147, 28.36831967535351, 0.0], [77.40416140548453, 28.37080235923333, 0], [77.40218550684746, 28.    3699755298779, 0.0], [77.40187364471585, 28.36769815943599, 0.0], [740486731638147, 28.36831967535351, 0.0]]]
      }}]}
polygon_list = [polygon1,polygon2]
union_data = heliGeoprocessingService.Union(apikey,polygon_list)

```
#### Polygon Intersection Example 

```
from heligeo import heliGeoprocessingService
apikey = ''
polygon1 = {"type": "FeatureCollection","features":[{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[77.4029103817493, 28.36918941103731, 0.0], [77.40184896262588, 28.3722403721131, 0.0][77.39922678901301, 28.37081966588294, 0.0], [77.40030856003351, 28.36816909494472, 0.0], [74029103817493, 28.36918941103731, 0.0]]]
  }}]}
polygon2 = {"type": "FeatureCollection","features":[{
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[77.40486731638147, 28.36831967535351, 0.0], [77.40416140548453, 28.37080235923333, 0], [77.40218550684746, 28.    3699755298779, 0.0], [77.40187364471585, 28.36769815943599, 0.0], [740486731638147, 28.36831967535351, 0.0]]]
      }}]}
polygon_list = [polygon1,polygon2]
intersection_data = heliGeoprocessingService.Intersection(apikey,polygon_list)
```

#### PointBuffer Example 
point_list accept multiple points data 
```
apikey = ''
point_list = [[88.3639,22.5726]] ### user can user multiple Point inside a list 
area = 100  ### how area user want to conver from this point by default its meter
point_buffer_polygon=heliGeoprocessingService.PointBuffer(apikey,point_list,area)

```

#### LineBuffer Example 
linestring_point_list accept multiple linestring.
```   

apikey = ''
linestring_point_list = [[[88.3639,22.5726],[88.4143,22.5797]],[[88.2636,22.5958],[88.4789,22.7248]]] ### usecan  user multiple Point inside a list 
area = 100  ### how area user want to conver from this point by default its meter
linestring_buffer_polygon=heliGeoprocessingService.LineBuffer(apikey,linestring_point_list,area)

```
#### PointWithinPoly Example 
```
apikey = ''
point_geojson_object = {"type":"FeatureCollection","features":[{"type":"Feature","geometry":                {"type":"Point","coordinates":[76.95513342,28.46301607]}}]}
polygon_list = [polygon1,polygon2]
point_inside_poly = heliGeoprocessingService.PointWithinPoly(apikey,point_geojson_object,polygon_list)

```
#### AliasLinestring Example 
```
apikey = ''
linestring_geojson_object = {"type": "FeatureCollection","features":[{"type": "Feature","geometry{"type":"LineString",
    "coordinates": [
      [88.3639,22.5726],[88.4143,22.5797]
    ]}}]}
gap = 100 #gap between multiple linestring(meter)
quantity = 100 ## how many line string u need 
alias_linestring_data = heliGeoprocessingService.AliasLinestring(apikey,linestring_geojson_object,gap,quantity)

```




## License
© 2021 HELIWARE

This repository is licensed under the MIT license. See LICENSE for details.