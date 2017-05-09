import sys
import os
import json

accessToken = "BQArY7HMG6veoiBFXuekpZdjeKnf-rvuwHgCHPVR425j2Bgx-HSBhCCwpov8UQAClxh8QG91R-deInaVlfH0euc4QnnwnQwuhFgf2l4ms19H03bcibt2I0fUqyzD_AaY96edveSjGu4iHAQgyMRf5qCqdQPwYfReaEbGutjnLSiJeI03mu2wuVrqh6fDtg"

userID = "kaizentowfiq"
#request = "curl -X GET 'https://api.spotify.com/v1/me/tracks' -H 'Authorization: Bearer " + accessToken +  "' > newData"
#output playlist file that holds song ids
request = "curl -X GET 'https://api.spotify.com/v1/users/" + userID + "/playlists' -H 'Authorization: Bearer " + accessToken + "'"
playlists = json.loads(os.system(request))
import pdb
pdb.set_trace()
