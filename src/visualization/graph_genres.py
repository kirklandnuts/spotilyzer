import pandas as pd
import numpy as np
import sys
from sklearn import preprocessing
from sklearn.decomposition import PCA
import plotly.plotly as py
import plotly.graph_objs as go

'''
Usage:
plotly must be set up for the graphing to work
------------------------------------------------
$ python graph_genres.py 2

         - OR -

$ python graph_genres.py 3 
------------------------------------------------
'''

def graph3DPlotlyCategoriesDifferentColors(df, features, categories):
    if len(features) == 3:
        traces = []
        for i in list(range(0,len(categories))):
            pdf = df[df["category"] == categories[i]]
            x = pdf[features[0]]
            y = pdf[features[1]]
            z = pdf[features[2]]
            traces.append(go.Scatter3d(
                x=x,
                y=y,
                z=z,
                name=categories[i],
                mode='markers',
                marker=dict(
                    size=12,
                    line=dict(
                        color='rgba(217, 217, 217, 0.14)',
                        width=0.5
                    ),
                    opacity=0.8
                )
            ))
        data = traces
        layout = go.Layout(
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0
            )
        )
        fig = go.Figure(data=data, layout=layout)
        py.plot(fig)
    else:
        print("need 3 features to do 3D graph")

def graph2DPlotlyCategoriesDifferentColors(df, features, categories):
    if len(features) == 2:
        traces = []
        for i in list(range(0,len(categories))):
            pdf = df[df["category"] == categories[i]]
            x = pdf[features[0]]
            y = pdf[features[1]]
            traces.append(go.Scatter(
                x=x,
                y=y,
                name=categories[i],
                mode='markers',
                marker=dict(
                    size=12,
                    line=dict(
                        color='rgba(217, 217, 217, 0.14)',
                        width=0.5
                    ),
                    opacity=0.8
                )
            ))
        data = traces
        layout = go.Layout(
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0
            )
        )
        fig = go.Figure(data=data, layout=layout)
        py.plot(fig)
    else:
        print("need 2 features to do 2D graph")

def PCAOnDataFrame(df, features, components):
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
        #normalize data
        for i in list(range(1,components+1)):
                min_max_scaler = preprocessing.MinMaxScaler()
                min_max_scaler.fit(newDataFrame[str(i)])
                newDataFrame[str(i)] = pd.DataFrame(min_max_scaler.transform(newDataFrame[str(i)]))
        return newDataFrame.set_index("songid")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        features = ["popularity", "danceability", "energy", "key", "loudness", "speechiness", "acousticness",
                                 "instrumentalness", "liveness", "valence", "tempo", "time_signature"]
        components = int(sys.argv[1])
        df = pd.read_csv('../../data/song_data_cleaned.csv')
        categories = df.category.unique().tolist()
        if components == 2:
            pcadf = PCAOnDataFrame(df, features, 2)
            graph2DPlotlyCategoriesDifferentColors(pcadf, ['1', '2'], categories)
        elif components == 3:
            pcadf = PCAOnDataFrame(df, features, 3)
            graph3DPlotlyCategoriesDifferentColors(pcadf, ['1', '2', '3'], categories)
        else:
            print("only graphing 2 dimensions or 3 dimensions")
    else:
        print("incorrect usage")
