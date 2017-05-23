# spotify-dashboard

learn about your Spotify usage and behavior

## Week 1 milestones
* Machine learning to build sound profiles for genres
* Run predictions of genre of new song
* May not be done in a day--meet twice (Monday 15th, Friday 19th)

### Week 1 discussion
* Want: a generalized framework with all data for future features
* Table that links playlists to songs and songs to playlists (all data that we could possibly need in the near future)
* Make subsets of playlists/tracks and do analysis on other songs

#### Database 
* getData module usage
once postgresql is installed on the machine you will be using, make sure to add a postgres user spotilyzer
with password spotipass that has permission to create databases.  Then, use getData to your heart's content.`


#### Defining musical profile
Motivation: given some playlists (generally well defined categories) and a song determine where the song 'best fits'. Also try to deterimine how well a song fits into a playlist in general. 
  
Given a playlist P, and model its corresponding 'musical profile' as such:

> Model each feature n as an independent normal random variable Xk for k = 1, 2, ... , n with mean and variation derived from all songs in the playlist with corresponding probability density function gk   
> Call the probability density function of all the random variables f(v)= g1(v1)\*g2(v2)\* ... \*gn(vn), where v = \[v1, v2, ... , vn\] is a vector of the corresponding feature values. This is the 'musical profile' of P  
> Define the 'musical fit' of a song v to a playlist x as f(v)  

Let P1, P2, ... ,Pn be n different playlists, and let f1, f2, ... , fn be their corresponding musical profiles. Let v be the song that we wish to match to a playlist. Then:

> The playlist that v fits best in is then defined as max(fi(v)) for all i = 1, 2, ... , n.  
> Define also 'close fits' for all j = 1, 2, ... , n as fj(v) >= r*fi(v) for some ratio 0 < r < 1  
> We can furthermore define confidence of best fit based off how close the next nearest fit(s) are  
> Also define fit into playlist based off of ratio of f(v) compared to max f(x), i.e. the 'peak' of the probability distribution function f.   

Based off this analysis, we can determine which playlist(s) most fit the profile of a song (e.g. genre) 

  
### Week 1 results
* Dataframe set up 
	* masterFrame['trackslist'][playlist index][song index][feature]
	* Gives feature value for song in playlist.
* Now that we have data week 2 will be fucking around with visualization and obtaining useful insights 

## Week 2 milestones
* Visualization day
	* Use pca to reduce to 3 dimensions
	* ^Sidenote, could we use some sort of coloring scheme to 'increase' the amount of dimensions
* Writing up inertia7 report

### Data modelling - Dimension reduction (PCA)
* Will need to talk with Kaisen about theory -Alex
* Reduces music data to 3d (magic)


### Drawing playlist/genre insights (Graphing)
* In progress, do on your own and do individual presentations wed.
* Use existing python code to use (Maybe Kaisen/Arthur write detailed explanations of methods? Will look at comments later to maybe do this part)


### Genre prediction
* In progress, maybe not this week
	* Good for once we have insights/some intuition about how music clustering works


## Future plans
* Endgame, after this quarter
* Create an api of sorts for artists?


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

### After (summer)
* Use get-audio-analysis with unsupervised machine learning to get deeper insights on data
* Cluster analysis with audio features and playlists
* Website
* Generate a playlist given a set of user profiles based off of analysis of individual musical taste (say for party)
	* Take a facebook event and match with spotify profiles and generate playlist for event


## Instructions
* The first time you run the node server, make sure to run 'npm install' before doing anything
* Will be updated and moved to top at the end of this project


## Architecture Overview

### Server
The server uses a cookie to figure out if the user is logged in.  If login cookie is present, it sends the userhome page. Otherwise, sends a basic splash page with a login button.  When a user logs in, the server relays the Spotify authorization tokens to the client, then adds the login cookie.  Authorization tokens are not stored serverside, simply sent to the client(through an object that's stringified and sent as an Express template local).  In general, you probably want to avoid changing any of the current routes.  Adding new ones is fine, though.

### Client
Every page(so far, at least) follows the basic template in layout.jade.  Vue.js is library of choice for our frontend because it's light, readable, and easy to learn with great documentation.  Authorization tokens are stored in the credentials object and are saved/updated to HTML5 localstorage automatically.
`
