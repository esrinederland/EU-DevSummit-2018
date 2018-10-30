#mvanhulzen_esrinl / 73c9697e1cdf469da1b683fb2263adeb
import requests

def generateAgolToken():
   
    username = "demo_user"
    password = "demo_password"
    tokenURL = "https://www.arcgis.com/sharing/generateToken"
     params = {'username': username, 'password': password, 'referer' : "http://www.arcgis.com", 'f' : 'json' }

    try:
        r = requests.get(tokenURL, params = params)


        agolToken = r.json()
        return agolToken
    except:
        agolToken = False
        return agolToken
