#-------------------------------------------------------------------------------
# Name:        getbeer
# Purpose:     to demo running REST API analyses
#
# Author:      mjagt
#
# Created:     07-10-2018
# Copyright:   (c) esri nederland bv 2018
#-------------------------------------------------------------------------------
import requests
import os
import json
import time
from Password import PassWord, UserName

print("Start - Get Beer Script")
   
### URL TO THE ESRI WORLD SERVICE AREA SERVICE
solveServiceAreaUrl = "https://route.arcgis.com/arcgis/rest/services/World/ServiceAreas/NAServer/ServiceArea_World/solveServiceArea"
### PORTAL ITEM THAT CONTAINS CONSUMER SALES LOCATIONS IN BERLIN
consumerSalesLocationsLayerUrl = "https://services.arcgis.com/emS4w7iyWEQiulAb/arcgis/rest/services/Locatus_Berlin/FeatureServer/0"

### GET A TOKEN
print("Getting token")
token_URL = "https://www.arcgis.com/sharing/generateToken"
token_params = {"username":UserName,"password": PassWord,"referer": "http://www.arcgis.com","f":"json","expiration":60}
r = requests.post(token_URL,token_params)
token_obj= r.json()
token = token_obj["token"]

### COORDINATES OF THE BCC BERLIN CONGRES CENTER
x = 13.416309
y = 52.521197

### SET THE DESIRED TRAVELMODE
travelMode = {
        "attributeParameterValues":
        [
                {
                        "parameterName":"Restriction Usage","attributeName":"Walking",
                        "value":"PROHIBITED"
                },
                {
                        "parameterName":"Restriction Usage","attributeName":"Preferred for Pedestrians",
                        "value":"PREFER_LOW"
                },
                {
                        "parameterName":"Walking Speed (km/h)","attributeName":"WalkTime","value":5
                }
        ],
        "description":"Follows paths and roads that allow pedestrian traffic and finds solutions that optimize travel time. The walking speed is set to 5 kilometers per hour.",
        "impedanceAttributeName":"WalkTime",
        "simplificationToleranceUnits":"esriMeters",
        "uturnAtJunctions":"esriNFSBAllowBacktrack",
        "restrictionAttributeNames":
        [
                "Preferred for Pedestrians","Walking"
        ],
        "useHierarchy":"false",
        "simplificationTolerance":2,
        "timeAttributeName":"WalkTime",
        "distanceAttributeName":"Miles",
        "type":"WALK",
        "id":"caFAgoThrvUpkFBW",
        "name":"Walking Time"
        }

### SET THE MAXIMUM TIME TO WALK
walkTime = 15

### PERFORM THE SOLVE SERVICE AREA REQUEST
print("Sending solve area request")
params = {"f" : "json",
        "facilities" : "{},{}".format(x,y),
        "travelMode" : json.dumps(travelMode),
        "defaultBreaks" : [walkTime],
        "token": token}

r = requests.post(solveServiceAreaUrl,params)
serviceArea = r.json()["saPolygons"]["features"][0]["geometry"]

### GET THE BARS (BEERS) FROM THE LAYER WITH CONSUMER SALES LOCATIONS
### USE THE SERVICE AREA GEOMETRY AS INPUT FO THE QUERY
print("Sending get bars request")
queryFeatureUrl = "{}/query".format(consumerSalesLocationsLayerUrl)
params = {"f" : "json",
        "where" : "RETAIL_ACTIVITY = '59.210.123-Pub'",
        "geometry" : json.dumps(serviceArea),
        "geometryType" : "esriGeometryPolygon",
        "inSR" : 4326,
        "returnGeometry" : "false",
        "outFields" : "NAME,STREET,HOUSE_NO,HOUSE_NO_ADDITION",
        "token": token}

r = requests.post(queryFeatureUrl,params)
beerLocations = r.json()["features"]

### PRINT THE FOUND BEER LOCATIONS TO THE CONSOLE
print("The following beer locations are within {} minutes walking from the BCC Berlin:".format(walkTime))
for location in beerLocations:
        print(u"{:15} | {} {} {}".format(location["attributes"]["NAME"], location["attributes"]["STREET"], location["attributes"]["HOUSE_NO"], location["attributes"]["HOUSE_NO_ADDITION"] if location["attributes"]["HOUSE_NO_ADDITION"] != None else ""))

print("script complete")