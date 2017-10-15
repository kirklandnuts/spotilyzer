#The purpose of this module is to handle the retrieval of all necessary data for the analysis programs
#Contributors: Kaizen Towfiq
import requests
import base64
import pdb
import re
import psycopg2
from psycopg2 import connect
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DBUSER = "spotilyzer"
DBPASS = "spotipass"
DBNAME = "spotilyzerdb"

#user functions
def getSongs(songList):
	#INPUT: takes a list of song id's
	#OUTPUT: returns a list
	con = None
	try:
		con = connect(dbname=DBNAME, user=DBUSER, host='localhost', password=DBPASS)
	except:
		__createDB()
		__createSongsTable()
		__createArtistsTable()
		__createAlbumsTable()

	try:
		con = connect(dbname=DBNAME, user=DBUSER, host='localhost', password=DBPASS)
	except:
		print("Failed to create DB")

	access_header = getAccessHeader()
	data = [] #using a list because we want to preserve order
	if con is not None:
		con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
		i = 0
		for songID in songList:
			i += 1
			if __dbHasSong(con, songID):
				songData = __querySong(songID, con)
				data.append(songData) #append the feature dctionary for the song
			else:
				songFeatures = __getSongFeatures(songID, access_header)
				if songFeatures is not None:
					#songAnalysis = getSongAnalysis(songID, access_header)
					trackInfo = __getTrack(songID, access_header)
					songData = {**trackInfo, **songFeatures}
					__insertSong(songData, con)
					data.append(songData)
				else:
					continue
			print("[" + str(i) + "/" + str(len(songList)) + "]" + "Got data for song: (" + songData["songid"] + ") " + songData["song_title"] + " by " + songData['artist_name'])
	else:
		print("No connection to database")
	return data

def getSongsInCategory(category):
	con = None
	try:
		con = connect(dbname=DBNAME, user=DBUSER, host='localhost', password=DBPASS)
	except:
		__createDB()
		__createSongsTable()
		__createArtistsTable()
		__createAlbumsTable()

	try:
		con = connect(dbname=DBNAME, user=DBUSER, host='localhost', password=DBPASS)
	except:
		print("Failed to create DB")

	data = []
	access_header = getAccessHeader()
	if con is not None:
		categoryIDs = __getCategories(access_header)
		categoryPlaylistIDs = __getCategoryPlaylists(categoryIDs[category], access_header)
		allSongIDs = []
		for i in categoryPlaylistIDs:
			songs = __getPlaylistSongIDs(i, access_header)
			allSongIDs = allSongIDs + songs
		uniqueSongIDs = set(allSongIDs)
		data = getSongs(uniqueSongIDs)
	else:
		print("No connection to database")
	return data

def getAllSongsInDB():
	con = None
	try:
		con = connect(dbname=DBNAME, user=DBUSER, host='localhost', password=DBPASS)
	except:
		print("Can't connect to DB. does it exist?")
	songs = []
	if con is not None:
		con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
		cur = con.cursor()
		query = "SELECT * FROM songs"
		cur.execute(query)
		resp = cur.fetchall()
		for songQuery in resp:
			sd = {}
			sd["songid"] = songQuery[0]
			sd["artistids"] = songQuery[1]
			sd["albumid"] = songQuery[2]
			sd["song_title"] = songQuery[3]
			sd["available_markets"] = songQuery[4]
			sd["duration"] = songQuery[5]
			sd["popularity"] = songQuery[6]
			sd["danceability"] = songQuery[7]
			sd["energy"] = songQuery[8]
			sd["key"] = songQuery[9]
			sd["loudness"] = songQuery[10]
			sd["mode"] = songQuery[11]
			sd["speechiness"] = songQuery[12]
			sd["acousticness"] = songQuery[13]
			sd["instrumentalness"] = songQuery[14]
			sd["liveness"] = songQuery[15]
			sd["valence"] = songQuery[16]
			sd["tempo"] = songQuery[17]
			sd["time_signature"] = songQuery[18]
			sd["artist_name"] = songQuery[19]
			songs.append(sd)
		cur.close()

	return songs

def getArtists(artistList):
	return

def getAlbums(albumList):
	return

def getAccessHeader():
	TOKEN_URL = "https://accounts.spotify.com/api/token"
	CLIENT_ID = "fa7e7c8d114a487c81a31a32dd0c0ef5"
	CLIENT_SECRET = "7df74727c0a846b1ba7bf042f9421f6c"
	DATA = {"grant_type":"client_credentials"}
	temp1 = CLIENT_ID+":"+CLIENT_SECRET
	temp2 = temp1.encode('utf-8','strict')
	HEADER_64_STRING = base64.b64encode(temp2)
	HEADERS = {"Authorization":b"Basic "+HEADER_64_STRING}
	response = requests.post(TOKEN_URL, data=DATA, headers=HEADERS)
	response.content
	access_token = response.json()['access_token']
	access_header = {"Authorization":"Bearer "+access_token}
	return access_header

#Helper functions
def __insertSong(songData, con):
	cur = con.cursor()
	sd = songData
	sd['song_title'] = re.sub("'", "", sd['song_title'])
	for i in sd.keys():
		if sd[i] is None:
			sd[i] = 0
	values = "('%s', '{%s}', '%s', '%s', '{%s}', %d, %d, %f, %f, %d, %f, %d, %f, %f, %f, %f, %f, %f, %d, '%s')" % \
				(sd["songid"], ','.join(sd["artistids"]), sd["albumid"], sd["song_title"], ','.join(sd["available_markets"]),sd["duration"], sd["popularity"], sd["danceability"], sd["energy"], sd["key"], sd["loudness"], sd["mode"], sd["speechiness"], sd["acousticness"], sd["instrumentalness"], sd["liveness"], sd["valence"], sd["tempo"], sd["time_signature"], sd['artist_name'].replace("'",""))
	insertCommand = "INSERT INTO songs (songid, artistids, albumid, song_title, available_markets, duration, popularity, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature, artist_name) VALUES " + values
	cur.execute(insertCommand)
	cur.close()

def __querySong(sid, con):
    cur = con.cursor()
    query = "SELECT * FROM songs WHERE songid='" + sid + "'"
    cur.execute(query)
    songQuery = cur.fetchone()
    sd = {}
    sd["songid"] = songQuery[0]
    sd["artistids"] = songQuery[1]
    sd["albumid"] = songQuery[2]
    sd["song_title"] = songQuery[3]
    sd["available_markets"] = songQuery[4]
    sd["duration"] = songQuery[5]
    sd["popularity"] = songQuery[6]
    sd["danceability"] = songQuery[7]
    sd["energy"] = songQuery[8]
    sd["key"] = songQuery[9]
    sd["loudness"] = songQuery[10]
    sd["mode"] = songQuery[11]
    sd["speechiness"] = songQuery[12]
    sd["acousticness"] = songQuery[13]
    sd["instrumentalness"] = songQuery[14]
    sd["liveness"] = songQuery[15]
    sd["valence"] = songQuery[16]
    sd["tempo"] = songQuery[17]
    sd["time_signature"] = songQuery[18]
    sd["artist_name"] = songQuery[19]
    cur.close()
    return sd

def __getCategories(access_header):
	url = "https://api.spotify.com/v1/browse/categories"
	resp = requests.get(url, headers=access_header).json()
	categoryToID = {}
	for i in resp["categories"]["items"]:
		categoryToID[i["name"]] = i["id"]
	return categoryToID

def __getCategoryPlaylists(cid, access_header):
	url = "https://api.spotify.com/v1/browse/categories/" + cid +"/playlists"
	resp = requests.get(url, headers=access_header).json()
	pids = []
	for i in resp["playlists"]["items"]:
		pids.append(i["id"])
	return pids

def __getPlaylistSongIDs(pid, access_header):
	url = "https://api.spotify.com/v1/users/spotify/playlists/" + pid
	resp = requests.get(url, headers=access_header)
	songIDs = []
	if resp.status_code == 200:
		for i in resp.json()["tracks"]["items"]:
			songIDs.append(i["track"]["id"])
	return songIDs

def __getSongFeatures(sid, access_header):
    url = "https://api.spotify.com/v1/audio-features/" + sid
    resp = requests.get(url, headers=access_header)
    songFeatures = resp.json()
    try:
        songFeatures["duration"] = songFeatures["duration_ms"]
        songFeatures["songid"] = songFeatures["id"]
        del songFeatures["type"]
        del songFeatures["uri"]
        del songFeatures["track_href"]
        del songFeatures["analysis_url"]
        del songFeatures["duration_ms"]
        del songFeatures["id"]
        return songFeatures
    except:
        print("nothing to delete")
        return None

def __getSongAnalysis(sid, access_header):
	url = "https://api.spotify.com/v1/audio-analysis/" + sid
	resp = requests.get(url, headers=access_header)
	songAnalysis = resp.json()
	return songAnalysis

def __getTrack(sid, access_header):
    url = "https://api.spotify.com/v1/tracks/" + sid
    resp = requests.get(url, headers=access_header)
    trackInfo = resp.json()
    track = {}
    track["song_title"] = trackInfo["name"]
    #currently only getting the first artist, may need to change later to handle multiple
    track["artistids"] = []
    track["artist_name"] = trackInfo['album']['artists'][0]['name']
    for i in trackInfo["artists"]:
        track["artistids"].append(i["id"])
    track["albumid"] = trackInfo["album"]["id"]
    track["available_markets"] = trackInfo["available_markets"]
    track["popularity"] = trackInfo["popularity"]
    return track

def __dbHasSong(con, sid):
	con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = con.cursor()
	cur.execute("SELECT * FROM songs WHERE songid='" + sid + "'")
	row = cur.fetchone()
	cur.close()
	return row is not None

def __createDB():
    print("==== Instantiating database")
    con = connect(dbname='postgres', user=DBUSER, host='localhost', password=DBPASS)
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute('CREATE DATABASE ' + DBNAME)
    cur.close()
    con.close()

def __createSongsTable():
	con = connect(dbname=DBNAME, user=DBUSER, host='localhost', password=DBPASS)
	con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = con.cursor()
	query = """CREATE TABLE songs(songID char(22) PRIMARY KEY NOT NULL,
			artistIDs char(22)[] NOT NULL,
			albumID char(22) NOT NULL,
			song_title varchar NOT NULL,
			available_markets char(2)[],
			duration int,
			popularity int,
			danceability double precision,
			energy double precision,
			key int,
			loudness double precision,
			mode int,
			speechiness double precision,
			acousticness double precision,
			instrumentalness double precision,
			liveness double precision,
			valence double precision,
			tempo double precision,
                        time_signature int,
                        artist_name varchar NOT NULL)"""
	cur.execute(query)
	cur.close()
	con.close()

def __createArtistsTable():
	con = connect(dbname=DBNAME, user=DBUSER, host='localhost', password=DBPASS)
	con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = con.cursor()
	query = """CREATE TABLE artists(
    	ArtistID char[22] NOT NULL PRIMARY KEY,
    	followers int,
    	genres varchar[],
    	name varchar,
    	popularity int)"""
	cur.execute(query)
	cur.close()
	con.close()

def __createAlbumsTable():
	con = connect(dbname=DBNAME, user=DBUSER, host='localhost', password=DBPASS)
	con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = con.cursor()
	query = """CREATE TABLE albums(
  		albumID char(22) PRIMARY KEY NOT NULL,
  		artistIDs char(22)[] NOT NULL,
  		songIDs char(22)[] NOT NULL,
   		album_title varchar NOT NULL,
  		available_markets char(2)[],
   		popularity int,
  		genres varchar[],
  		release_date varchar,
  	 	release_date_precision varchar,
   		label varchar);"""
	cur.execute(query)
	cur.close()
	con.close()

FEATURES = ["popularity", "danceability", "energy", "key", "loudness", "speechiness", "acousticness",
                                 "instrumentalness", "liveness", "valence", "tempo", "time_signature"]
COLUMNS = ["songid", "song_title", "artist_name", "popularity", "danceability", "energy", "key", \
            "loudness", "speechiness", "acousticness", "instrumentalness", "liveness", \
            "valence", "tempo", "time_signature", "category"]
GENRES = ['Pop', 'Electronic/Dance', 'Hip-Hop', 'Rock', 'Indie', 'R&B', 'Metal', 'Soul', 'Romance', 'Jazz']

if __name__ == "__main__":
    ACCESS_HEADER = getAccessHeader() 
    categories = list(__getCategories(ACCESS_HEADER).keys())
    preFrameDict = {}
    for i in FEATURES:
        preFrameDict[i] = []
    preFrameDict["songid"] = []
    preFrameDict["category"] = []
    for i in categories:
        print("==== Getting data for songs from category " + i)
        songs = getSongsInCategory(i)
        for j in songs:
            preFrameDict["category"].append(i)
            preFrameDict["songid"].append(j["songid"])
            for q in FEATURES:
                preFrameDict[q].append(j[q])
    df = pd.DataFrame(preFrameDict)
    df = df[COLUMNS]
    df = df[df.category.isin(categories)]
    df.to_csv('./song_data.csv', index = False)
