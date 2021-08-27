# Spotify Song Recommender

Like a song on Spotify? Find a similar new song or enjoy an old favorite!

# What is it?

Spotify Song Recommender is a web app that allows a user to input an artist and a song and receive 6 recommendations fo songs with similar audio features.


## Where to find it?

[Spotify Song Recommender](https://share.streamlit.io/galtman5/spotify-app/main/webapp.py) | 
[Product Vision Document](https://docs.google.com/document/d/1KPL0QsSkWh8R6L73XGzA4TYLI9MfM3HPKGD3IUiCuHo/edit?usp=sharing)

## How was it built?

This web app is built in Python and depolyed on Streamlit. The app uses a K-Nearest Neighbors model to generate recommendations.

## Main Features
    
Uses the following inputs to generate recommendations:
- Artist Name
- Song Name

Upon receipt of the inputs, the app queries the Spotify API to download the audio features of the song. These include:
- Acousticness: a confidence measure from 0.0 to 1.0 of whether the song is acoustic.
- Danceability: describes how suitable a song is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity.
- Energy: a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy.
- Explicit: whether or not the song has explicit content.
- Instrumentalness: predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”.
- Key: maps to pitches using standard Pitch Class notation . E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on.
- Liveness: detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live
- Loudness: the overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). 
- Mode: indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived.
- Speechiness: detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.
- Tempo: the overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.	
- Time_signature: an estimated overall time signature of a track. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure).
- Valence: a measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).

Output:
- 6 recommendations of songs that have similar audio features as the input song. We chose 6 songs because for songs that are included in the training database, the K-Nearest Neighbors model returns the input song as the first recommended song (given that the input song has 0 euclidean distance from itself).
- A visualization highlighting the similarities and differences in the audio features of the input song and second recommended song. 

## Contributors

Thanks to the following people who have contributed to this project:

* [@Guy Altman](https://github.com/galtman5)
* [@Ivan Mihailov](https://github.com/ivan-mihailov)
* [@Jonathan Krier](https://github.com/jkriertran)
* [@Youssef Al-Yakoob](https://github.com/yalyakoob)

## License
[MIT](https://choosealicense.com/licenses/mit/)
