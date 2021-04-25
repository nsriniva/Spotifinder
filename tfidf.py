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

for song in data:
  str_song = pd.Series(song).item()
  new_data.append(str_song)

tfidf = TfidfVectorizer(stop_words='english',
                        ngram_range=(1,2),
                        min_df=3,
                        max_df=0.25)



#Create a vocabulary and get word counts per document
dtm = tfidf.fit_transform(new_data)

#Get feature names to use as dataframe column headers
dtm = pd.DataFrame(dtm.todense(), columns=tfidf.get_feature_names())
