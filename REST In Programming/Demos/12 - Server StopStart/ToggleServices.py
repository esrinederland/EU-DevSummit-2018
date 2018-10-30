#-------------------------------------------------------------------------------
# Name:        ToggleServices
# Purpose:     to demo the rest api of arcgis server
#
# Author:      mvanhulzen
#
# Created:     15-10-2018
# Copyright:   (c) Esri Nederland BV 2018
#-------------------------------------------------------------------------------
import requests
import Security
import datetime

_serverurl = "http://localhost:6080/arcgis/admin"
_action = "stop"; #can be start or stop
def main():
    
    #generate a token on arcgis for server
    token = GetToken()

    #get a list of all services from the server
    servicesUrl = "{}/services?f=json&token={}".format(_serverurl,token)
    r = requests.get(servicesUrl)
    services = r.json()

    #for a list of all services from the server
    for service in services["services"]:
        if service== services["services"][2]:
            print("We are not going to stop our {}".format(service["serviceName"]))
        else:
            print("Set service {} to {}".format(service["serviceName"],_action))

            serviceActionUrl = "{}/services/{}.{}/{}?f=json&token={}".format(_serverurl,service["serviceName"],service["type"],_action,token)

            r = requests.post(serviceActionUrl)

            print("result: {}".format(r.text))

    print("Script complete")

def GetToken():

    token_url = "{}/generateToken".format(_serverurl)
    token_params = {'username':Security.Server_UserName,'password': Security.Server_Password,'client': 'requestip','f':'json','expiration':60}
    print("requesting token with username: {}".format(Security.Server_UserName))
    r = requests.post(token_url,token_params)
        
    print("Resultcode: {}".format(r.status_code))
    token_obj= r.json()
        
    token = token_obj['token']
    expires = token_obj['expires']

    tokenExpires = datetime.datetime.fromtimestamp(int(expires)/1000)

    print("token for user {}, valid till: {} : {}".format(Security.Server_UserName,tokenExpires,token))
    return token  

if __name__ == "__main__":
    main()