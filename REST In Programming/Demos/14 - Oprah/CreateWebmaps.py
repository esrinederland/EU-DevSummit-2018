#-------------------------------------------------------------------------------
# Name:        CreateWebmaps
# Purpose:     to demo the creation of a webmap per feature
#
# Author:      mvanhulzen
#
# Created:     15-10-2018
# Copyright:   (c) Esri Nederland BV 2018
#-------------------------------------------------------------------------------

import requests
import json
import Security
import copy


templatewebmapid = "b9f6548c35b242f7bd357851f78d0c44"
layerUrl = "https://services.arcgis.com/emS4w7iyWEQiulAb/arcgis/rest/services/survey123_a0986d8d8c354d5d85ab796fe8ddb763/FeatureServer/0"

print("getting token")
token = Security.generateToken()

defaultParams = {"f":"json","token":token}

print("getting template webmap")
webmapInfoUrl = "https://www.arcgis.com/sharing/rest/content/items/b9f6548c35b242f7bd357851f78d0c44"
r = requests.get(webmapInfoUrl,defaultParams)
webmapInfo = r.json()

webmapDataUrl = f"{webmapInfoUrl}/data"
r = requests.get(webmapDataUrl,defaultParams)
webmapData = r.json()

print("getting folder id")
folderid = webmapInfo["ownerFolder"]

print("get features from service")
queryParams = defaultParams.copy()
queryParams["where"] = "1=1"
queryParams["outFields"] =  "*"

queryUrl = f"{layerUrl}/query"
r = requests.get(queryUrl,queryParams)
surveyValues = r.json()["features"]

for feature in surveyValues:
    name = feature["attributes"]["Name"]
    oid = feature["attributes"]["ObjectId"]
    nice = feature["attributes"]["Something_nice"]
    print("Creating webmap for {}".format(feature["attributes"]["Name"]))

    newWebmapData = copy.deepcopy(webmapData)
    newWebmapData["operationalLayers"][0]["layerDefinition"]["definitionExpression"] = f"ObjectID={oid}"

    webmapInfo = defaultParams.copy()
    webmapInfo["title"] = f"Generated webmap for {name}"
    webmapInfo["tags"] = f"EUDevSummit2018Generated,REST,Demo,{name}"
    webmapInfo["description"] = f"Hello {name}, this is a newly created webmap. You said: {nice}"
    webmapInfo["type"] = "Web Map"
    webmapInfo["text"] = json.dumps(newWebmapData)

    addItemurl = f"https://www.arcgis.com/sharing/rest/content/users/{Security.UserName}/{folderid}/addItem"

    r = requests.post(addItemurl,webmapInfo)

    print(r.text)