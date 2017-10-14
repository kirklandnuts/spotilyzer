import getData as gd

allFeatures = ["popularity", "danceability", "energy", "key", "loudness", "speechiness", "acousticness",
                 "instrumentalness", "liveness", "valence", "tempo", "time_signature"]

accessHeader = gd.getAccessHeader()
categories = list(gd.__getCategories(accessHeader).keys())

import pdb
pdb.set_trace()

