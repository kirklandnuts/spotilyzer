#The purpose of this module is to handle the retrieval of all necessary data for the analysis programs
import requests
import base64
import pdb
import psycopg2
from psycopg2 import connect
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DBUSER = "spotilyzer"
DBPASS = "spotipass"
DBNAME = "spotilyzerdb"

def getSongs(songList):
	#INPUT: takes a list of song id's
	#OUTPUT: returns a list
	con = None
	try:
		con = connect(dbname=DBNAME, user=DBUSER, host='localhost', password=DBPASS)
	except:
		createDB()
		createSongsTable()
		createArtistsTable()
		createAlbumsTable()

	try:
		con = connect(dbname=DBNAME, user=DBUSER, host='localhost', password=DBPASS)
	except:
		print("Failed to create DB")
	
	access_header = getAccessHeader()
	if con is not None:
		con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
		data = [] #using a list because we want to preserve order
		for songID in songList:
			if dbHasSong(con, songID):
				songData = querySong(songID, con)
				data.append(songData) #append the feature dctionary for the song
			else:
				songFeatures = getSongFeatures(songID, access_header)
				#songAnalysis = getSongAnalysis(songID, access_header)
				trackInfo = getTrack(songID, access_header)
				songData = {**trackInfo, **songFeatures}
				insertSong(songData, con)
				data.append(songData)
	else:
		print("No connection to database")

	return data

def insertSong(songData, con):
	cur = con.cursor()
	sd = songData
	values = "('%s', '%s', '%s', '%s', '{%s}', %d, %d, %f, %f, %d, %f, %d, %f, %f, %f, %f, %f, %f, %d)" % \
				(sd["id"], sd["artistid"], sd["albumid"], sd["name"], ','.join(sd["available_markets"]),sd["duration_ms"], sd["popularity"], sd["danceability"], sd["energy"], sd["key"], sd["loudness"], sd["mode"], sd["speechiness"], sd["acousticness"], sd["instrumentalness"], sd["liveness"], sd["valence"], sd["tempo"], sd["time_signature"])
	insertCommand = "INSERT INTO songs (songid, artistids, albumid, song_title, available_markets, duration, popularity, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature) VALUES " + values
	pdb.set_trace()
	cur.execute(insertCommand)
	cur.close()

def querySong(sid, con):
	cur = con.cursor()
	query = "SELECT * FROM songs WHERE songid='" + sid + "'"
	cur.execute(query)
	songData = cur.fetchone()
	return songData
	

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

def getSongFeatures(sid, access_header):
	url = "https://api.spotify.com/v1/audio-features/" + sid
	resp = requests.get(url, headers=access_header)
	songFeatures = resp.json()
	del songFeatures["type"]
	del songFeatures["uri"]
	del songFeatures["track_href"]
	del songFeatures["analysis_url"]
	return songFeatures

def getSongAnalysis(sid, access_header):
	url = "https://api.spotify.com/v1/audio-analysis/" + sid
	resp = requests.get(url, headers=access_header)
	songAnalysis = resp.json()
	return songAnalysis

def getTrack(sid, access_header):
	url = "https://api.spotify.com/v1/tracks/" + sid
	resp = requests.get(url, headers=access_header)
	trackInfo = resp.json()
	track = {}
	track["name"] = trackInfo["name"]
	#currently only getting the first artist, may need to change later to handle multiple
	track["artistid"] = trackInfo["artists"][0]["id"]
	track["albumid"] = trackInfo["album"]["id"]
	track["available_markets"] = trackInfo["available_markets"]
	track["popularity"] = trackInfo["popularity"]
	return track
	
def dbHasSong(con, sid):
	con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = con.cursor()
	cur.execute("SELECT * FROM songs WHERE songid='" + sid + "'")
	row = cur.fetchone()
	cur.close()
	return row is not None

def createDB():
	con = connect(dbname='postgres', user=DBUSER, host='localhost', password=DBPASS)
	con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = con.cursor()
	cur.execute('CREATE DATABASE ' + DBNAME)
	cur.close()
	con.close()

def createSongsTable():
	con = connect(dbname=DBNAME, user=DBUSER, host='localhost', password=DBPASS)
	con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = con.cursor()
	query = """CREATE TABLE songs(songID char(22) PRIMARY KEY NOT NULL,
			artistIDs char(22) NOT NULL,
			albumID char(22) NOT NULL,
			song_title text NOT NULL,
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
			tempo double precision,time_signature int)"""
	cur.execute(query)
	cur.close()
	con.close()

def createArtistsTable():
	con = connect(dbname=DBNAME, user=DBUSER, host='localhost', password=DBPASS)
	con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = con.cursor()
	query = """CREATE TABLE artists(
    	ArtistID char[22] NOT NULL PRIMARY KEY,
    	followers int,
    	genres text[],
    	name text,
    	popularity int)"""
	cur.execute(query)
	cur.close()
	con.close()

def createAlbumsTable():
	con = connect(dbname=DBNAME, user=DBUSER, host='localhost', password=DBPASS)
	con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = con.cursor()
	query = """CREATE TABLE albums(
  		albumID char(22) PRIMARY KEY NOT NULL,
  		artistIDs char(22)[] NOT NULL,
  		songIDs char(22)[] NOT NULL,
   		album_title text NOT NULL,
  		available_markets char(2)[],
   		popularity int,
  		genres text[],
  		release_date text,
  	 	release_date_precision text,
   		label text);"""
	cur.execute(query)
	cur.close()
	con.close()
