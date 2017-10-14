# Loading
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import linear_model, metrics
from sklearn.grid_search import GridSearchCV
from sklearn import preprocessing
import pickle


features = ["popularity", "danceability", "energy", "loudness", "speechiness", "acousticness",
				 "instrumentalness", "liveness", "valence", "tempo"]



def subset_genre(tr, te, genres):
    """
    subsets training and test data to only include genres of interest
    """
    tr = tr.groupby(['category'])
    te = te.groupby(['category'])
    tr_list = []
    te_list = []
    for genre in genres:
    	tr_list.append(tr.get_group(genre))
    	te_list.append(te.get_group(genre))
    tr = pd.concat(tr_list)
    te = pd.concat(te_list)
    return tr, te


def score(pred, true):
    score = metrics.accuracy_score(true, pred)
    print(pd.crosstab(pred, true,
                      rownames=['Predicted Values'],
                      colnames=['True Values']))
    print("Accuracy: %f" % score)

if __name__ == '__main__':


    # load data
    tr = pd.read_csv('/Users/timmy/Documents/data-sci/github/spotilyzer/spotilyzer/song-data-tr.csv')
    te = pd.read_csv('/Users/timmy/Documents/data-sci/github/spotilyzer/spotilyzer/song-data-te.csv')
    # subset data
    # full ['Pop', 'Electronic/Dance', 'Hip-Hop', 'Indie', 'Metal', 'Jazz']
    genres = ['Pop', 'Electronic/Dance', 'Hip-Hop' ,'Metal', 'Jazz']
    tr, te = subset_genre(tr, te, genres)

    print('==== scaling data')
    scaler = preprocessing.StandardScaler().fit(tr[features])
    tr_scaled = pd.DataFrame(scaler.transform(tr[features]))
    te_scaled = pd.DataFrame(scaler.transform(te[features]))

    # coarse-tuning
    print('==== Tuning on coarse grid')
    Cbase = 10.0
    tuning_params = [{'C': Cbase**np.arange(-4,4)}]
    clf = GridSearchCV(linear_model.LogisticRegression(), tuning_params, cv=5)
    clf.fit(tr_scaled, tr.category)

    pred = clf.predict(te_scaled)
    score(pred, te.category)

    # fine-tuning
    print('==== Tuning on fine grid')
    Cbase_fine = clf.best_params_['C']
    tuning_params_fine = [{'C': np.arange(Cbase_fine/10.0, Cbase_fine*10.0, Cbase_fine/2)}]
    clf2 = GridSearchCV(linear_model.LogisticRegression(), tuning_params_fine, cv=5)
    clf2.fit(tr_scaled, tr.category)

    pred = clf2.predict(te_scaled)
    score(pred, te.category)

    # Train finalized classifier
    print('==== Tuning final model')
    Copt = clf2.best_params_['C']
    clf_final = linear_model.LogisticRegression(random_state=101, C=Copt)
    clf_final.fit(tr_scaled, tr.category)

    # pickling model
    file_name = './LR.pickle'
    file_object = open(file_name, 'wb')
    pickle.dump(clf_final, file_object)

    # predict
    pred = clf_final.predict(te_scaled)
    score(pred, te.category)
