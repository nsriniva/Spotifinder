import pandas as pd
import numpy as np
from re import compile as rcompile
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.optimizers import Adam, Nadam
from sklearn.neighbors import NearestNeighbors
from joblib import load
from zipfile import ZipFile
from os.path import dirname

DIR = dirname(__file__)

rex = rcompile('[^a-zA-Z 0-9]')

tokenize = lambda x: rex.sub('', x.lower().replace(',', ' '))

MODELS_DIR = DIR + '/../../models/'
DATA_DIR = DIR + '/../../data/'

ENCODER = 'encoder.h5'
FG_ENCODER = 'fg_encoder.h5'

ENCODER_PATH = MODELS_DIR + ENCODER + '.zip'
ENCODED_DTM = MODELS_DIR + 'encoded_dtm.pkl'
TFIDF = MODELS_DIR + 'tfidf.pkl'

FG_ENCODER_PATH = MODELS_DIR + FG_ENCODER 
FG_ENCODED_DF = MODELS_DIR + 'fg_encoded_df.pkl'
GENRES_TFIDF = MODELS_DIR + 'genres_tfidf.pkl'
SCALER = MODELS_DIR + 'scaler.pkl'


TRACKS = DATA_DIR + 'tracks_genres_lyrics_en.csv.zip'

class FindSongs(object):
    def __init__(self):
        
        with ZipFile(ENCODER_PATH, 'r') as zipObj:
           zipObj.extractall()
        
        self.encoder = load_model(ENCODER)
        self.tfidf = load(TFIDF)
        self.encoded_dtm = load(ENCODED_DTM)
        # Fit on DTM
        self.nn = NearestNeighbors(n_neighbors=5, algorithm='ball_tree')
        self.nn.fit(self.encoded_dtm)

        self.features = [
            'popularity', 'duration_ms', 'explicit', 'danceability',
            'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence',
            'tempo', 'time_signature'
        ]
        self.fg_encoder = load_model(FG_ENCODER_PATH)
        self.fg_encoded_df = load(FG_ENCODED_DF)
        self.genres_tfidf = load(GENRES_TFIDF)
        self.scaler = load(SCALER)
        self.fg_nn = NearestNeighbors(n_neighbors=5, algorithm='ball_tree')
        self.fg_nn.fit(self.fg_encoded_df)
        
        self.tracks_df = pd.read_csv(TRACKS)
        
        self.tracks_df.drop(columns=['Unnamed: 0'], inplace=True)
        self.tracks_df = self.tracks_df[self.tracks_df.genres.isna() == False]
        
    def find_song_entries(self, x):
        vec = self.tfidf.transform([tokenize(x)]).todense()
        encoded_vec = self.encoder.predict(vec)
        entries = self.nn.kneighbors(encoded_vec)[1][0].tolist()
        entries = self.tracks_df.iloc[entries].popularity.sort_values(ascending=False).index.tolist()
        
        return self.tracks_df.loc[entries]
    
    def find_song_entry(self, x, best_choice=True):
        df = self.find_song_entries(x)
    
        choice = df.index.tolist()
        if best_choice:
            choice = choice[0]
    
        return df.loc[choice]


    def get_recommendations(self, x):
        
        gvec = self.genres_tfidf.transform([tokenize(x.genres)]).todense()
        fvec = self.scaler.transform([x[self.features]])
        vec = [fvec.tolist()[0] + gvec.tolist()[0]]
        encoded_vec = self.fg_encoder.predict(vec)
        entries = self.fg_nn.kneighbors(encoded_vec)[1][0].tolist()
        entries = self.tracks_df.iloc[entries].popularity.\
            sort_values(ascending=False).index.tolist()
        
        return self.tracks_df.loc[entries]
