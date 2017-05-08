# spotify-dashboard
learn about your Spotify usage and behavior

## Driving questions
* How do I define my current musical taste?
* What's my next favorite band/artist?

## Instructions
* The first time you run the node server, make sure to run 'npm install' before doing anything

## Architecture Overview

### Server
The server uses a cookie to figure out if the user is logged in.  If login cookie is present, it sends the userhome page. Otherwise, sends a basic splash page with a login button.  When a user logs in, the server relays the Spotify authorization tokens to the client, then adds the login cookie.  Authorization tokens are not stored serverside, simply sent to the client(through an object that's stringified and sent as an Express template local).  In general, you probably want to avoid changing any of the current routes.  Adding new ones is fine, though.

### Client
Every page(so far, at least) follows the basic template in layout.jade.  Vue.js is library of choice for our frontend because it's light, readable, and easy to learn with great documentation.  Authorization tokens are stored in the credentials object and are saved/updated to HTML5 localstorage automatically.
