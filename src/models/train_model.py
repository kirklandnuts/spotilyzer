#!/usr/bin/env python3
######################
#Kaizen Towfiq

import sys
import pickle
import pandas as pd
from sklearn import preprocessing
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

'''
USAGE:

$ python train_model.py RF
$ python train_model.py LR
'''

def create_RF_model(training_set, test_set,  target, test_targert, componentsList, estimators):
	classifier = RandomForestClassifier(max_features=None, n_estimators=estimators)
	classifier.fit(training_set[componentsList], target)
	file_Name = "RF.pickle"
	fileObject = open(file_Name,'wb')
	pickle.dump(classifier,fileObject)   
	fileObject.close()

def create_LR_model():
    pass

categories = ['Jazz', 'Rock', 'Hip-Hop', 'Metal', 'Electronic/Dance', 'Pop']
allFeatures = ["popularity", "danceability", "energy", "loudness", "speechiness", "acousticness",
				 "instrumentalness", "liveness", "valence", "tempo"]

if __name__ == '__main__':
    if len(sys.argv) == 2:
        model = sys.argv[1]
        test_set = pd.read_csv('../data/song_data_te.csv')
        training_set = pd.read_csv('../data/song_data_tr.csv')
        training_group = training_set.groupby(['category'])
        test_group = test_set.groupby(['category'])
        
        tr_list = []
        te_list = []
        
        for genre in categories:
            tr_list.append(training_group.get_group(genre))
            te_list.append(test_group.get_group(genre))
        
        training_set = pd.concat(tr_list)
        test_set = pd.concat(te_list)
        target = training_set['category']
        test_target = test_set['category']
        if model == 'RF':
            create_RF_model(training_set, test_set, target, test_target, allFeatures, 5000)
        elif model == 'LR':
            create_LR_model()
        else:
            print("supported models:  RF, LR")
    else:
        print("incorrect usage")
