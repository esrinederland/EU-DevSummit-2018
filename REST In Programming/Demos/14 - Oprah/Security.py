import requests
UserName = "demo_user"
def generateToken():
    
    password = "demo_password"
    tokenURL = "https://www.arcgis.com/sharing/generateToken"
    
    params = {'username': UserName, 'password': password, 'referer' : "http://www.arcgis.com", 'f' : 'json' }

    try:
        r = requests.get(tokenURL, params = params)

        agolToken = r.json()
        return agolToken["token"]
    except:
        agolToken = False
        return agolToken
