import requests
import psycopg2
from psycopg2 import connect
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DBUSER = "spotilyzer"
DBPASS = "spotipass"
DBNAME = "spotilyzerdb"

def test():
	print("success")

def getSongs(songList, **kwargs):
	#INPUT: takes a list of song id's, kwargs: accessToken, userID
	#OUTPUT: returns a list
	con = None
	try:
		con = connect(dbname=DBNAME, user=DBUSER, host='localhost', password=DBPASS)
	except:
		createDB()
		createSongsTable()
		createArtistsTable()
		createAlbumsTable()
	
	if con:
		featureData = []
		for songID in songList:
			if dbHasSong(con, songID):
				 featureData.append({}) #append the feature dctionary for the song
			else:
				#query api
				featureData.append({})
				#insert data into db
	else:
		print("No connection to database")

	return featureData
	
def dbHasSong(con, sid):
	cur = con.cursor()
	con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur.execute("SELECT * FROM songs WHERE songid='" + sid + "';")
	row = cur.fetchone()
	import pdb
	pdb.set_trace()
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
	return

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
	return
