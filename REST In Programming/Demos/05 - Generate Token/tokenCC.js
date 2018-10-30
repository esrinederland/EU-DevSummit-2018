var request = require('request'); // npm install request

// generate a token with your client id and client secret
request.post({
    url: 'https://www.arcgis.com/sharing/rest/oauth2/token/',
    json: true,
    form: {
      'f': 'json',
      'client_id': 'cient_id',
      'client_secret': 'client_secret',
      'grant_type': 'client_credentials',
      'expiration': '1440'
    }
}, function(error, response, body){
    console.log(body.access_token);
});