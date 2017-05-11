# spotify-dashboard
learn about your Spotify usage and behavior

## Driving questions
* How do I define my current musical taste?
* What's my next favorite band/artist?

### Analysis Features
* Fit within a playlist -e.g. distance from rest of playlist
* Potentially optimal order
* Metrics of playlist 
	* Variability of each variable, e.g. danceability
	* Stacked area chart for change of variables - visualization of a new song into a playlist
* Color code playlists and plot all songs of each - divide up 'music space' into playlist domains and new songs naturally fit into a playlist
	* Implications of how 'mixed' playlists turn out to be?

### 

###After (summer)
* Use get-audio-analysis with unsupervised machine learning to get deeper insights on data
* Cluster analysis with audio features and playlists
* Website
* Generate a playlist given a set of user profiles based off of analysis of individual musical taste (say for party)
	* Take a facebook event and match with spotify profiles and generate playlist for event


## Instructions
* The first time you run the node server, make sure to run 'npm install' before doing anything

## Architecture Overview

### Server
The server uses a cookie to figure out if the user is logged in.  If login cookie is present, it sends the userhome page. Otherwise, sends a basic splash page with a login button.  When a user logs in, the server relays the Spotify authorization tokens to the client, then adds the login cookie.  Authorization tokens are not stored serverside, simply sent to the client(through an object that's stringified and sent as an Express template local).  In general, you probably want to avoid changing any of the current routes.  Adding new ones is fine, though.

### Client
Every page(so far, at least) follows the basic template in layout.jade.  Vue.js is library of choice for our frontend because it's light, readable, and easy to learn with great documentation.  Authorization tokens are stored in the credentials object and are saved/updated to HTML5 localstorage automatically.
`