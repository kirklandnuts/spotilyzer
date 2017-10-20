
# spotify-dashboard

learn about your Spotify usage and behavior  
Note: the top part will be a report on what this does and how.  
**To do (5/31/2017)**

## Introduction
Use Spotify API to obtain song information (e.g. tempo, popularity, key, energy, danceability, etc.)


## Usage
Dependencies in requirements.txt  
(Not too sure of how much detail we need, could make slow walkthrough of installation of dependencies and getting data. Also could make a template for people to get started -Alex)


## Spotify API
Getting audio features, (basically getData.py)  


## Database 
PostgreSQL database, api calls to get song data (also getData.py)


## Data Visualization 
PCA and ggplot


## Machine learning
KNN  


# Spring 2017 
Reverse chronological log of project evolution. Missing week 3 (whoops). 
## Future plans
All unrealized ideas to date that can segue into main project well (add everything we've missed)
   
* Playlist generation from set of playlists
* Build a 'musical profile'
* Analyse song order in a playlist, define metrics/features for playlists 


## Final update (milestones) - 5/31/2017

### Getting data
* Now able to obtain 15,000+ songs (Takes forever beware)
* Categorized by song category (similar to spotify)
* To do: Make SQL Dump of data (Kaizen)


### Analysis/Graphing
Have used PCA to reduce dimensions, then plot data - see spotilyzer. Motivation of following programs:

* graphFeaturedPlaylists.py  
	* **Motivation:** First plotting code, shows that dataframe and plotting behaves as expected. Attempts to use PCA to make data understandable.
	* **Methods:** Implementation of pandas dataframe for song data. PCA on dataframe and reformatting (normalisation) of new data for creation of a PCA'd dataframe. Use of ggplot to visualize data, with methods for 2D and 3D graphing (cycles through different colors for different playlists).
	* **Results:** Showed that we could begin visualizing data. Opened the door for general data-fuckery.
	* **To do:** Reuse code on new stuff to fuck with data. Implementation of more robust coloring scheme.


* relationAnalysis.py 
	* **Motivation:** Graphing playlists via PCA on songs is ineffective. Trying to PCA where we only consider variation between playlists may yield better results
	* **Methods:** Takes the mean of each feature in each playlist, and does PCA on that set. Then uses the same PCA and transforms the original dataframe. Returns the transformed dataframe.
	* **Results:** Somewhat more clear clustering. Some playlists were still all over the place. Unsure whether from ambiguous data or ineffective PCA
	* **To do:** More distinctions between playlists/categories in final graph, e.g. Nice sexy plot with little overlap between tight clusters

* predictCategoryKNN.py 
	* **Motivation:** Begin attempting proof of concept for music genre prediction via K-nearest neighbors(KNN). 
	* **Methods:** Uses scikit-learn KNN module. Currently running with default settings and n_neighbors=500 on categories jazz, rock, chill. 
	* **Results:** Can get ~70% accuracy with 3 categories, ~90% accuracy with 2. 
	* **To do:** Use different modifiers to train algorithm better. Perhaps find categories with larger differences to see how it does. Goal: See how well KNN can do optimally, and under what modifiers/datasets. 


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



## Driving questions (Planning)
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
