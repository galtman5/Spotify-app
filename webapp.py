import streamlit as st
import streamlit.components.v1 as components
import requests

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


if len(user_artist) & len(user_song) > 0:
    url = 'search?q=artist:' + name_cleaner(user_artist) + \
        '%20track:' + user_song + '&type=track'

    r = requests.get(BASE_URL + url, headers=headers)
    track_id = r.json()['tracks']['items'][0]['id']

    html_string = '''<iframe src="https://open.spotify.com/embed/track/''' + track_id + '''"
    width="300" height="380" frameborder="0" 
    allowtransparency="true" allow="encrypted-media"></iframe>'''

    st.markdown(html_string, unsafe_allow_html=True)
