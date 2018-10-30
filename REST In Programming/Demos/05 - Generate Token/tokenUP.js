var request = require('request'); // npm install request

// generate a token with your client id and client secret
request.post({
    url: 'https://www.arcgis.com/sharing/generateToken',
    json: true,
    form: {
      'f': 'json',
      'username': 'username',
      'password': 'password',
      'referer': 'http://www.arcgis.com',
      'expiration': '1440'
    }
}, function(error, response, body){
    console.log(body.token);
});