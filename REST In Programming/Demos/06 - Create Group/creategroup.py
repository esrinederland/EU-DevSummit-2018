import requests
import json
from Password import UserName, PassWord

print("Start - Creating Groups")

### GET A TOKEN
print("Getting token")
token_URL = "https://www.arcgis.com/sharing/generateToken"
token_params = {"username":UserName,"password": PassWord,"referer": "http://www.arcgis.com","f":"json","expiration":60}
r = requests.post(token_URL,token_params)
token_obj= r.json()
token = token_obj["token"]

### SET THE GROUP PARAMETERS
print("Creating group parameters")
newGroupName = "Demo Group"
newGroupDesc = "Group to show how to create groups"
newGroupParams = {'title':newGroupName,'access':'account','description':newGroupDesc, "isViewOnly":True,"isInvitationOnly":True,"tags":"EUDevSummit2018"}

url='https://www.arcgis.com/sharing/rest/community/createGroup?f=json&token={}'.format(token)

### SEND THE REQUEST TO CREATE THE GROUP
print("Sending request")
r = requests.post(url,newGroupParams)
print(r.json())

print("Script complete")