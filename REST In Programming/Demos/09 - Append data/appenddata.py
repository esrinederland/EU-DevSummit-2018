#-------------------------------------------------------------------------------
# Name:        appenddata
# Purpose:     to demo the appending of data to a feature service
#
# Author:      mholtslag
#
# Created:     07-10-2018
# Copyright:   (c) esri nederland bv 2018
# Licence:     
#-------------------------------------------------------------------------------
import zipfile
import os
import json
import requests
import sys
import time
from Security import *

def main():
    print("Appending data to feature")

    portalUrl = "http://www.arcgis.com"
    username = "mvanhulzen_esrinl"

    #upload zip gdb
    fileName = "European_Cities_Part2.gdb.zip"
    objectName = os.path.split(fileName)[-1]
    fileType = "File Geodatabase"
    
    currentID = getPortalIdByNameAndType(objectName, fileType)

    if currentID != None:
        addUrl = '{}/sharing/rest/content/users/{}/items/{}/update'.format(portalUrl, username, currentID)
    else:
        addUrl = "{}/sharing/rest/content/users/{}/addItem".format(portalUrl,username)

    filesUp = {"file": open(fileName, 'rb')}

    token = generateAgolToken()["token"]

    params = {}
    params["f"] = "json"
    params["token"] = token
    params["filename"] = fileName
    params["type"] = fileType
    params["title"] = objectName
    params["tags"] = "European cities,Dev Summit 2018,Part2"
    params["description"] = "Part 2 of European cities for Dev Summit 2018"

    print("Start uploading {} to Arcgis Online".format(fileName))
    
    response = requests.post(addUrl, params, files=filesUp)
    itemPartJSON = response.json()

    if "success" in itemPartJSON:
        zipid = itemPartJSON['id']

    print("Zipfile added to content: {}".format(zipid))
    
    #appendparameters
    layerUrl = "https://services.arcgis.com/emS4w7iyWEQiulAb/arcgis/rest/services/European_Cities_2018/FeatureServer/0"

    params = {}
    params["f"] = "json"
    params["token"] = token
    response = requests.post(layerUrl, params)
    layerInfo = response.json()

    dctSource, fields = getFieldMappings(layerInfo)

    #APPEND
    print("Appending data to: {}".format(layerInfo["name"]))

    appendUrl = "{}/append".format(layerUrl)

    params = {}
    params["f"] = "json"
    params["token"] = token
    params["sourceTableName"] = "European_Cities_Part2"
    params["fieldMappings"] = json.dumps(dctSource)
    params["upsert"] = False
    params["skipUpdates"] = False
    params["useGlobalIds"] = False
    params["skipInserts"] = False
    params["updateGeometry"] = True
    params["appendItemId"] = zipid
    params["appendUploadFormat"] = "filegdb"
    params["rollbackOnFailure"] = True
    params["appendFields"] = json.dumps(fields)

    response = requests.post(appendUrl, params)
    append = response.json()
    
    #JOBSTATUS
    status = "InProgress"
    while (status == "InProgress" or status == "Pending"):
        print("Status is {}, sleeping for 5 seconds".format(status))
        time.sleep(5)
        params = {}
        params["f"] = "json"
        params["token"] = token
        try:
            response = requests.post(append["statusUrl"], params)
            status = response.json()["status"] 
        except Exception as e:
            time.sleep(5)
            response = requests.post(append["statusUrl"], params)
            status = response.json()["status"] 
            pass
    
    print("Status is: {}".format(status))
    if status != "Completed":
        if status == "Failed":
            print("Failed updating data")
        else:
            print("Not completed with status code: {}".format(status))
    else:
        print("Succesfully updated layer {}".format(layerInfo["name"]))

def getFieldMappings(layerInfo):
    fields = [x["name"] for x in layerInfo["fields"]]

    fields.remove(layerInfo["objectIdField"])

    if "Shape__Area" in fields:
        fields.remove("Shape__Area")
    if "Shape__Length" in fields:
        fields.remove("Shape__Length")

    dctSource = [{"source":x,"name":x} for x in fields] 
    return dctSource, fields

def getPortalIdByNameAndType(name,typeName):

    username = "mvanhulzen_esrinl"
    wherestring = 'title:"{}" AND type:"{}" AND owner:"{}"'.format(name,typeName,username)
    results = searchPortalItems(wherestring)
    returnID = None
    if len(results) > 0:
        returnID = results[0]["id"]
        print(typeName + " exists, id: " + returnID)
    else:
        print(typeName + " does not exist")
    return returnID

def searchPortalItems(wherestring, start=1):
    token = generateAgolToken()["token"]
    questionParams = {'q':wherestring, "sortField":"name","start":start, "num":100, "f":"json", "token":token}
    url = r"{}/sharing/rest/search".format("http://www.arcgis.com")
    print("Start searching portal: {}, start: {}".format(wherestring,start))
    response = requests.post(url,questionParams, verify=False)
    retObject = response.json()
    returnResults = []
    if retObject["total"] > 0:
        returnResults = retObject["results"]
      
    else:
        print("No results for wherestring: {}".format(wherestring))
    return returnResults

if __name__=="__main__":
    main()
