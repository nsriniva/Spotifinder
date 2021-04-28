import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

spotify_songs = pd.read_csv("data/spotify_songs.csv.zip")

def clean_data(data):
    # drop nulls in lyrics column
    data = data.dropna()

    # Only get songs with lyrics in English
    data = data[data['language'] == 'en']

    # Drop duplicates
    data = data.drop_duplicates(subset=['track_name', 'track_artist'],
                                keep='first')

    # Reduce features
    features = ['track_id', 'track_name', 'track_artist', 'lyrics']
    data = data[features]

    # Reset index
    data = data.reset_index()

    return data

df = clean_data(spotify_songs)


def gather_data(songs):
    data =[]
    for song in songs:
        data.append(df['lyrics'][df['track_id'] == song])

    new_data = []

    for song in data:
        str_song = pd.Series(song).item()
        new_data.append(str_song)

    return new_data

songs = df['track_id']

data = gather_data(songs)

tfidf = TfidfVectorizer(stop_words='english',
                        ngram_range=(1,2), min_df=0.03,
                        max_df=0.25)

#Create a vocabulary and get word counts per document
#dtm = tfidf.fit_transform(new_data)
dtm = tfidf.fit_transform(data)

#Get feature names to use as dataframe column headers
#dtm = pd.DataFrame(dtm.todense(), columns=tfidf.get_feature_names())
dtm = pd.DataFrame(dtm.todense(), columns=tfidf.get_feature_names())

