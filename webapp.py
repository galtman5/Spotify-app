import joblib
from zipfile import ZipFile
import re
import feature_engine
import sklearn
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from feature_engine.encoding import OneHotEncoder as fe_OneHotEncoder

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


st.header("Spotify Song Recommender")
st.write("Directions: Enter the name of both the artist and song. We will throw a similar song back at you.")
user_artist = st.text_input('Enter an artist')
user_song = st.text_input('Enter a song')


def explicit_binarizer(x):
    if x == True:
        return 1
    else:
        return 0


def decade_function(x):
    if x in range(1900, 1991):
        return '1900-1990'
    elif x in range(1991, 1996):
        return '1991-1995'
    elif x in range(1996, 2001):
        return '1996-2000'
    elif x in range(2001, 2006):
        return '2001-2005'
    elif x == 2006:
        return '2006'
    elif x == 2007:
        return '2007'
    elif x == 2008:
        return '2008'
    elif x == 2009:
        return '2009'
    elif x == 2010:
        return '2010'
    elif x == 2011:
        return '2011'
    elif x == 2012:
        return '2012'
    elif x == 2013:
        return '2013'
    elif x == 2014:
        return '2014'
    elif x == 2015:
        return '2015'
    elif x == 2016:
        return '2016'
    elif x == 2017:
        return '2017'
    elif x == 2018:
        return '2018'
    elif x == 2019:
        return '2019'
    elif x == 2020:
        return '2020'
    elif x == 2021:
        return '2021'


def wrangle(df):
    #df.drop(columns='Unnamed: 0', inplace=True)
    df['explicit'] = df['explicit'].apply(explicit_binarizer)
    df['age'] = df['year'].apply(decade_function)
    loaded_ohe = joblib.load('ohe.joblib')
    df = loaded_ohe.transform(df.fillna('Missing'))
    # feature scailing for float columns in df3
    loaded_scaler = joblib.load('scaler.joblib')
    scale_cols = ['danceability', 'energy', 'loudness', 'speechiness',
                  'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                  'time_signature', 'key', 'mode']
    scaled = df[scale_cols].reset_index(drop=True)
    scaler = loaded_scaler
    scaled_float_df = pd.DataFrame(
        scaler.transform(scaled), columns=scaled.columns)
    df.drop(columns=scale_cols, inplace=True)
    df = pd.concat([df, scaled_float_df], axis=1)
    df.drop(columns='year', inplace=True)
    return df


def name_cleaner(track):
    return track.replace(" ", "+")


def year_cleaner(year):
    return year[:4]


def get_track_response():
    return requests.get(BASE_URL + url, headers=headers)


def get_track_id():
    track_response = get_track_response()
    track_id = track_response.json()['tracks']['items'][0]['id']
    return track_id


def get_track_features():
    url_features = 'audio-features/' + get_track_id()
    return requests.get(
        BASE_URL + url_features, headers=headers)


url = 'search?q=artist:' + name_cleaner(user_artist) + \
    '%20track:' + user_song + '&type=track'


def create_features_list():
    features = []

    for key, value in get_track_features().json().items():
        features.append(key)
        if key == 'tempo':
            break

    # add time_signature metric
    features.append('time_signature')

    # add the release year metric
    features.append('year')

    # only keep the year from the date. "2007-09-11" -> "2007"
    clean_year = year_cleaner(get_track_response().json()[
        'tracks']['items'][0]['album']['release_date'])

    # add explicit metric
    features.append('explicit')
    return features


def create_metrics_list():
    feature_metrics = []
    for key, value in get_track_features().json().items():
        feature_metrics.append(value)
        if key == 'tempo':
            break

    feature_metrics.append(get_track_features().json()['time_signature'])

    clean_year = year_cleaner(get_track_response().json()[
        'tracks']['items'][0]['album']['release_date'])
    feature_metrics.append(clean_year)

    feature_metrics.append(get_track_response().json()[
        'tracks']['items'][0]['explicit'])

    return feature_metrics


# main
if len(user_artist) & len(user_song) > 0:
    # create dataframe with the f
    feature_metrics = create_metrics_list()
    features = create_features_list()

    features_tracks_df = pd.DataFrame(
        data=[feature_metrics], columns=features)
    wrangled_features_tracks_df = wrangle(features_tracks_df)

    # Load pickled model and recommendations lookup dataframe
    knn_loader = joblib.load('ml/knn_model.joblib')
    file = 'data/df_rec_lookup.zip'

    # Load unwrangled dataset to match the song.
    with ZipFile(file, 'r') as zip:
        zip.extractall()
    df_rec_lookup = pd.read_csv('df_rec_lookup.csv')

    # Query Using kneighbors
    __, neigh_index = knn_loader.kneighbors(wrangled_features_tracks_df)

    # Instantiate song list
    song_list = []
    rec_id = []

    for i in neigh_index[0][:3]:
        rec_id.append(df_rec_lookup['id'][i])

    # create spotify embedder for first 3 songs that are reccomended
    for i in range(3):
        html_string = '''<iframe src="https://open.spotify.com/embed/track/''' + rec_id[i] + '''"
        width="230" height="320" frameborder="0" 
        allowtransparency="true" allow="encrypted-media"></iframe>'''
        st.markdown(html_string, unsafe_allow_html=True)

    st.write("The metrics of your song:")
    st.dataframe(features_tracks_df)

jon = '''<h1>Jonathan Krier</h1><a href="https://www.linkedin.com/in/jonathankrier/" target="_blank">LinkedIn</a>'''
yousef = '''<h1>Youssef Al-Yakoob</h1><a href="https://www.linkedin.com/in/youssefalyakoob/" target="_blank">LinkedIn</a><br><a href="https://github.com/yalyakoob" target="_blank">GitHub</a>'''
ivan = '''<h1>Ivan Mihailov</h1><a href="https://www.linkedin.com/in/ivan-mihailov/" target="_blank">LinkedIn</a><br><a href="https://github.com/ivan-mihailov" target="_blank">GitHub</a>'''
guy = '''<h1>Guy Altman</h1><a href="https://www.linkedin.com/in/guy-altman-970b70213/" target="_blank">LinkedIn</a><br><a href="https://github.com/galtman5" target="_blank">GitHub</a>'''

st.sidebar.title("The Team")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")

st.sidebar.markdown(jon, unsafe_allow_html=True)
st.sidebar.markdown(yousef, unsafe_allow_html=True)
st.sidebar.markdown(ivan, unsafe_allow_html=True)
st.sidebar.markdown(guy, unsafe_allow_html=True)
