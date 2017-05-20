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
	createDB(DBUSER, DBPASS)

def createDB(usr, pw):
	con = connect(dbname='postgres', user=usr, host='localhost', password=pw)
	con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = con.cursor()
	cur.execute('CREATE DATABASE ' + DBNAME)
	cur.close()
	con.close()

createDB('spotilyzer', 'spotipass')
