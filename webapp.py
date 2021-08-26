import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd

CLIENT_ID = '44e889b5f36f4da49f3abfaec8d5dba2'
CLIENT_SECRET = 'e6c5d8615afc46349a572570abbf211d'


AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'


st.header("Spotify Song Reccommender")
st.write("Directions: Enter the name of both the artist and song. We will throw a similar song back at you.")

user_artist = st.text_input('Enter an artist')
user_song = st.text_input('Enter a song')

#artist = 'kanye+west'
#track = 'stronger'


def name_cleaner(track):
    return track.replace(" ", "+")


def year_cleaner(year):
    return year[:4]


if len(user_artist) & len(user_song) > 0:
    url = 'search?q=artist:' + name_cleaner(user_artist) + \
        '%20track:' + user_song + '&type=track'

    # get the track id
    track_response = requests.get(BASE_URL + url, headers=headers)
    track_id = track_response.json()['tracks']['items'][0]['id']

    # get the track features
    url_features = 'audio-features/' + track_id
    feature_response = requests.get(BASE_URL + url_features, headers=headers)

    # make list of features and the metrics
    feature_metrics = []
    features = []

    for key, value in feature_response.json().items():
        feature_metrics.append(value)
        features.append(key)
        if key == 'tempo':
            break

    # add time_signature metric
    features.append('time_signature')
    feature_metrics.append(feature_response.json()['time_signature'])

    # add the release year metric
    features.append('year')
    # only keep the year from the date. "2007-09-11" -> "2007"
    clean_year = year_cleaner(track_response.json()[
        'tracks']['items'][0]['album']['release_date'])
    feature_metrics.append(clean_year)

    # add explicit metric
    features.append('explicit')
    feature_metrics.append(track_response.json()[
        'tracks']['items'][0]['explicit'])

    # create dataframe
    features_tracks_df = pd.DataFrame(data=[feature_metrics], columns=features)

    # create spotify embedder
    html_string = '''<iframe src="https://open.spotify.com/embed/track/''' + track_id + '''"
    width="300" height="380" frameborder="0" 
    allowtransparency="true" allow="encrypted-media"></iframe>'''

    st.markdown(html_string, unsafe_allow_html=True)
    st.dataframe(features_tracks_df)
