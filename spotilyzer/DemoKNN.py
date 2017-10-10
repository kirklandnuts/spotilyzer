#!/usr/bin/env python3
######################
#Kaizen Towfiq

import getData as gd
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve # ROC Curves
from sklearn.metrics import auc # Calculating AUC for ROC's!

def PCAOnDataFrameOld(df, features, components):
    pca = PCA(n_components=components)
    pca.fit(df[features])
    newData = pca.transform(df[features])
    preFrameDict = {}
    preFrameDict["songid"] = []
    preFrameDict["category"] = []
    for i in list(range(1,components+1)):
        preFrameDict[str(i)] = []
    for i in list(range(0, len(newData))):
        preFrameDict["songid"].append(df.index.tolist()[i])
        preFrameDict["category"].append(df["category"][i])
        for j in list(range(0,components)):
            preFrameDict[str(j+1)].append(newData[i][j])
    newDataFrame = pd.DataFrame(preFrameDict)
    return newDataFrame.set_index("songid")

def PCAOnDataFrame(training_set, test_set, features, components):
	pca = PCA(n_components=components, random_state=7)
	pca.fit(training_set[features])
	training_set_pca = pca.fit_transform(training_set[features])
	components_col = [x for x in range(0, components)]
	training_set = pd.DataFrame(training_set_pca, columns = components_col)

	test_set_pca = pca.transform(test_set[features])
	test_set = pd.DataFrame(test_set_pca, columns = components_col)
	return training_set, test_set, components_col

def createCategoriesDataFrame(categories, features):
	preFrameDict = {}
	for i in features:
		preFrameDict[i] = []
	preFrameDict["songid"] = []
	preFrameDict["category"] = []
	for i in categories:
		songs = gd.getSongsInCategory(i)
		for j in songs:
			preFrameDict["category"].append(i)
			preFrameDict["songid"].append(j["songid"])
			for q in features:
				preFrameDict[q].append(j[q])
	df = pd.DataFrame(preFrameDict)
	#normalize data
	train, test = train_test_split(df, test_size = 0.2, random_state=7)
	
	std_scale = preprocessing.MinMaxScaler().fit(train[features])
	train_trans = std_scale.fit_transform(train[features])
	training_set = pd.DataFrame(train_trans, columns = features)
	target = train['category']
	test_trans =  std_scale.transform(test[features])
	test_set = pd.DataFrame(test_trans, columns = features)
	test_targert = test['category']
	return df.set_index("songid"), training_set, test_set, target, test_targert

def predictCategoryKNN(training_set, test_set,  target, test_targert, componentsList, k):
	classifier = KNeighborsClassifier(n_neighbors=k, metric='minkowski')
	classifier.fit(training_set[componentsList], target)
	return test_set, classifier.predict(test_set[componentsList]), test_targert, classifier.score(test_set[componentsList], test_targert)

categories = ["Jazz", "Rock"] 
allFeatures = ["popularity", "danceability", "energy", "key", "loudness", "speechiness", "acousticness",
				 "instrumentalness", "liveness", "valence", "tempo", "time_signature"]

cdf, training_set_trans, test_set_trans, target, test_targert = createCategoriesDataFrame(categories, allFeatures)

training_set, test_set, components_col = PCAOnDataFrame(training_set_trans, test_set_trans, allFeatures, 2)

#testing KNN on pcadf
testdf, predictions, correctValues, score = predictCategoryKNN(training_set, test_set, target, test_targert, components_col, 83)


print(pd.crosstab(predictions, correctValues,
                  rownames=['Predicted Values'],
                  colnames=['Actual Values']))

print("Score: " + str(score))
#
#cv_df = pd.DataFrame(correctValues)
##
#pd_df = pd.DataFrame(predictions)
#
#pred_bin = pd_df[0] .map({'Jazz':1, 'Rock':0})
#
#corr_bin = cv_df['category'].map({'Jazz':1, 'Rock':0})
#
#
#fpr3, tpr3, _ = roc_curve(pred_bin, corr_bin)
#auc_knn = auc(fpr3, tpr3)
#
#f, ax = plt.subplots(figsize=(11, 11))
#	
#
#plt.plot(fpr3, tpr3,label='KNN ROC Curve (area = {0: .3f})'\
#    .format(auc_knn), 
#         color = 'purple', 
#         linestyle=':', 
#         linewidth=3)
#
#ax.set_facecolor('#fafafa')
#plt.plot([0, 1], [0, 1], 'k--', lw=2)
#plt.plot([0, 0], [1, 0], 'k--', lw=2, color = 'black')
#plt.plot([1, 0], [1, 1], 'k--', lw=2, color = 'black')
#plt.xlim([-0.01, 1.0])
#plt.ylim([0.0, 1.05])
#plt.xlabel('False Positive Rate')
#plt.ylabel('True Positive Rate')
#plt.title('ROC Curve Comparison For All Models')
#plt.legend(loc="lower right")
