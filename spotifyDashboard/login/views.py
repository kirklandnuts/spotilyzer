# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import spotipy

# Create your views here.
def index(request):
	
	lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
	
	spotify = spotipy.Spotify()
	results = spotify.artist_top_tracks(lz_uri)
	return HttpResponse(results['tracks'][0]['name'])
