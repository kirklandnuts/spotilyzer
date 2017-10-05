import getData as gd
import requests
import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from sklearn import preprocessing
from sklearn.decomposition import PCA
from matplotlib import style
import itertools
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve # ROC Curves
from sklearn.metrics import auc # Calculating AUC for ROC's!
import plotly.plotly as py
import plotly.graph_objs as go



categories = ['Jazz', 'Rock', 'Hip-Hop', 'Metal', 'Electronic/Dance', 'Pop']
allFeatures = ["popularity", "danceability", "energy", "loudness", "speechiness", "acousticness",\
                 "instrumentalness", "liveness", "valence", "tempo"]

df = pd.read_csv('song-data-unique.csv')

song_ids = df.songid.tolist()

song_data = gd.getSongs(song_ids)

sids = []
artists = []
names = []
categories = []

for sd in song_data:
	sids.append(sd['songid'])
	names.append(sd['song_title'])
	artists.append(sd['artistids'])
	categories.append(df[df.songid==sd['songid']].category.tolist()[0])

preFrameDict = {'songid':sids,
				'artist':artists,
				'name':names,
				'category':categories}
	
fdf = pd.DataFrame(preFrameDict)

fdf.to_csv('for_timmy.csv')
import pdb
pdb.set_trace()
