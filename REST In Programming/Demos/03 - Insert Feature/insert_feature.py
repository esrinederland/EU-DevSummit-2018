#-------------------------------------------------------------------------------
# Name:        insert_feature
# Purpose:     to demo the insertion of features in an arcgis online featureservice
#
# Author:      mvanhulzen
#
# Created:     07-10-2018
# Copyright:   (c) esri nederland bv 2018
#-------------------------------------------------------------------------------
import requests
import json

featureLayerUrl = "https://services.arcgis.com/emS4w7iyWEQiulAb/arcgis/rest/services/survey123_a0986d8d8c354d5d85ab796fe8ddb763_fieldworker/FeatureServer/0"

def main():
    print("Start insert_feature")
    
    x = 13.416309
    y = 52.521197

    print("Creating Feature")
    features = []

    feature = {}
    feature["attributes"] = {}
    feature["attributes"]["Name"] = "Maarten"
    feature["attributes"]["Country"] = "Netherlands"
    feature["attributes"]["Rating"] = "Five"
    feature["attributes"]["Something_nice"] = "Nice :)"

    feature["geometry"] = {}
    feature["geometry"]["x"] = x
    feature["geometry"]["y"] = y
    feature["geometry"]["spatialReference"] = {"wkid" : 4326}

    features.append(feature)

    print("sending request")
    addFeatureUrl = "{}/AddFeatures".format(featureLayerUrl)
    params = {'features':json.dumps(features),'f':'json'}
        
    r = requests.post(addFeatureUrl,params)

    print(r.text)

    print("script complete")

if __name__ == '__main__':
    main()
