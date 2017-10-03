import getData as gd

allFeatures = ["popularity", "danceability", "energy", "key", "loudness", "speechiness", "acousticness",
                 "instrumentalness", "liveness", "valence", "tempo", "time_signature"]

accessHeader = gd.getAccessHeader()
categories = gd.__getCategories(accessHeader)
