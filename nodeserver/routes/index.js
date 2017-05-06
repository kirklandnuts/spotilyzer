var express = require('express');
var router = express.Router();
var request = require('request'); // "Request" library
var querystring = require('querystring');
var cookieParser = require('cookie-parser');

const CLIENT_ID = 'fa7e7c8d114a487c81a31a32dd0c0ef5';
const CLIENT_SECRET = '7df74727c0a846b1ba7bf042f9421f6c';
const REDIRECT_URI = 'http://localhost:3000/callback';

const stateKey = 'spotify_auth_state';
var generateState = function () {
  return "teststate";
}

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Data Daddies' });
});

router.get('/logout', function(req, res, next) {
  res.clearCookie(stateKey);
  res.render('index', { title: 'Data Daddies (logged out)' });
});

router.post('/login', function(req, res, next) {
  var state = generateState();
  var scope = 'user-read-private user-read-email';
  res.cookie(stateKey, state);
  res.redirect('https://accounts.spotify.com/authorize?' +
    querystring.stringify({
      response_type: 'code',
      client_id: CLIENT_ID,
      scope: scope,
      redirect_uri: REDIRECT_URI,
      state: state
    }));
});

router.get('/callback', function(req, res) {
  var code = req.query.code || null;
  var state = req.query.state || null;
  var storedState = req.cookies ? req.cookies[stateKey] : null;
  if (state === null || state !== storedState) {
    redirect('/#'+
      querystring.stringify({
        error: 'state_mismatch'
      }));
  } else {
    res.clearCookie(stateKey);
    var authOptions = {
      url: 'https://accounts.spotify.com/api/token',
      form: {
        code: code,
        redirect_uri: REDIRECT_URI,
        grant_type: 'authorization_code'
      },
      headers: {
        'Authorization': 'Basic ' + (new Buffer(CLIENT_ID + ':' + CLIENT_SECRET).toString('base64'))
      },
      json: true
    };

    request.post(authOptions, function(error, response, body) {
      if (!error && response.statusCode === 200) {
        var access_token = body.access_token,
          refresh_token = body.refresh_token;
        var options = {
          url: 'https://api/spotify.com/v1/me',
          headers: { 'Authorization': 'Bearer '+access_token },
          json: true
        };

        request.get(options, function(error, response, body) {
          console.log(body);
        });
        res.redirect('/#'+
          querystring.stringify({
            access_token: access_token,
            refresh_token: refresh_token
          }));
      } else {
        res.redirect('/#'+
          querystring.stringify({
            error: 'invalid_token'
          }));
      }
    });
  }
});

router.get('/refresh_token', function(req, res) {
  var refresh_token = req.query.refresh_token;
  var authOptions = {
    url: 'https://accounts.spotify.com/api/token',
    headers: { 'Authorization': 'Basic '+(new Buffer(CLIENT_ID + ':' + CLIENT_SECRET).toString('base64'))},
    form: {
      grant_type: 'refresh_token',
      refresh_token: refresh_token
    },
    json: true
  };
  request.post(authOptions, function(error, response, body) {
    if (!error && response.statusCode === 200) {
      var access_token = body.access_token;
      res.send({
        'access_token': access_token
      });
    }
  });
});

module.exports = router;
