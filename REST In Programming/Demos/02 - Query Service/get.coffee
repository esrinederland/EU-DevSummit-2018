request = require 'request'

response = ""
request.get {uri:'https://services.arcgis.com/emS4w7iyWEQiulAb/arcgis/rest/services/European_Cities_2018_readonly/FeatureServer/0/query?where=1=1&returnCountOnly=true&f=json', json : true}, (error, response, body) ->
  console.log "The service contains " + body.count + " features"