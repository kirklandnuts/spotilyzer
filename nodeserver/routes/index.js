var express = require('express');
var router = express.Router();
var request = require('request'); // "Request" library
var querystring = require('querystring');

const CLIENT_ID = 'fa7e7c8d114a487c81a31a32dd0c0ef5';
const CLIENT_SECRET = '7df74727c0a846b1ba7bf042f9421f6c';
const REDIRECT_URI = 'http://localhost:3000/callback';
const APP_SCOPE = 'playlist-read-private';
const LOGIN_KEY = 'login_status';

const stateKey = 'spotify_auth_state';
var generateState = function () {
  return "teststate";
}

/* GET home page. */
router.get('/', function(req, res, next) {
  if (req.cookies[LOGIN_KEY]) {
    res.render('userhome');
  } else {
    res.render('index');
  }
});

router.get('/logout', function(req, res, next) {
  res.clearCookie(stateKey);
  res.clearCookie(LOGIN_KEY);
  res.redirect('/');
});

router.post('/login', function(req, res, next) {
  var state = generateState();
  res.cookie(stateKey, state);
  res.cookie(LOGIN_KEY, "true");
  res.redirect('https://accounts.spotify.com/authorize?' +
    querystring.stringify({
      response_type: 'code',
      client_id: CLIENT_ID,
      scope: APP_SCOPE,
      redirect_uri: REDIRECT_URI,
      state: state
    }));
});

router.get('/callback', function(req, res) {
  var code = req.query.code || null;
  var state = req.query.state || null;
  var storedState = req.cookies ? req.cookies[stateKey] : null;
  if (state === null || state !== storedState) {
    res.redirect('/#'+querystring.stringify({error: 'state_mismatch'}));
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
        var locals = {
          access_token: body.access_token,
          refresh_token: body.refresh_token
        }
        res.render('userhome', { data: JSON.stringify(locals) } );
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
