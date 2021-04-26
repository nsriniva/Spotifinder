import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

spotify_songs = pd.read_csv("data/spotify_songs.csv.zip")

spotify_songs = spotify_songs[spotify_songs['language']=='en']

df1 = spotify_songs.sort_values('track_popularity', ascending=False)[0:5000]


def gather_data(songs):
  data =[]
  for song in songs:
    data.append(spotify_songs['lyrics'][spotify_songs['track_id']==song])
  return data

songs = df1['track_id']

data = gather_data(songs)

new_data = []

pickle.load(nlp_dtm.pkl)
