"""Data visualization functions"""

from fastapi import APIRouter, HTTPException
import pandas as pd
import plotly.express as px

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from app import ml

import joblib
import pickle
from os.path import dirname

router = APIRouter()

stopwords = set(STOPWORDS)

DIR = dirname(__file__)
MODELS_DIR = DIR + '/../models/'
DATA_DIR = DIR + '/../data/'

data_filename = DATA_DIR + 'NLP_songs_data.zip'
model_filename = MODELS_DIR + 'nlp_model.pkl'
dtm_filename = MODELS_DIR + 'nlp_dtm.pkl'

df = None
loaded_model = None
dtm = None

def load_files():
    global df, loaded_model, dtm

    df = pd.read_csv(data_filename)
    loaded_model = pickle.load(open(model_filename, 'rb'))
    dtm = pickle.load(open(dtm_filename, 'rb'))


@router.get('/viz')
async def viz(artist, song):
    if dtm is None:
        load_files()

    #function to get 5 nearest songs
    def select_nearest_songs(artist, song):
        
        #translate artist, song into doc dtm.iloc[x].values
        artist_songs = df.loc[df['track_artist']==artist]
        selected_song = artist_songs.loc[artist_songs['track_name']==song]
        x = selected_song.index
        x = x[0]
        x = x.item()

        doc = dtm.loc[x].values
        result = loaded_model.kneighbors([doc], n_neighbors=6)
        
        rec_songs = {"artist":[], "song":[]};
        
        for i in range(5):
            song = result[1][0][1+i]

            #translate the loc into an artist and song title
            artist = df.loc[song]['track_artist']
            song = df.loc[song]['track_name']
            
            rec_songs['artist'].append(artist)
            rec_songs['song'].append(song)
        
        return rec_songs

    #Fetch lyrics function
    def get_lyrics(artist, song):
        songs_by_artist = df[['track_id','track_name']][df['track_artist'] == artist]
        song_id = songs_by_artist[songs_by_artist['track_name'] == song]
        song_id = song_id[:1] #This selects the first if there are more than one
        song_id = song_id['track_id']
        song_id = pd.Series(song_id).item()
        lyrics = df['lyrics'][df['track_id'] == song_id]
        lyrics = pd.Series(lyrics).item()

    #Print lyrics from both songs to compare
    song_recs = select_nearest_songs(artist, song)
    
    rec_artist = song_recs['artist'][0]
    rec_song = song_recs['song'][0]
    
    lyrics1 = get_lyrics(artist, song)
    lyrics2 = get_lyrics(rec_artist, rec_song)
    
    #Visualization Word Cloud
    def show_wordcloud(data, title = None):
        wordcloud = WordCloud(
            background_color='white',
            stopwords=stopwords,
            max_words=50,
            max_font_size=40,
            scale=3,
            random_state=37).generate(str(data))
        
        fig = plt.figure(1, figsize=(12,12))
        plt.axis('off')
        if title:
            fig.suptitle(title, fontsize=20)
            fig.subplots_adjust(top=2.3)
            
        plt.imshow(wordcloud)
        plt.show()

    return show_wordcloud(lyrics1), show_wordcloud(lyrics2)