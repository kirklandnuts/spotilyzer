var express = require('express');
var router = express.Router();

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

module.exports = router;
