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

ENCODER_PATH = MODELS_DIR + ENCODER + '.zip'
ENCODED_DTM = MODELS_DIR + 'encoded_dtm.pkl'
TFIDF = MODELS_DIR + 'tfidf.pkl'

TRACKS = DATA_DIR + 'tracks_genres_lyrics_en.csv.zip'

class FindSongs(object):
    def __init__(self):
        
        with ZipFile(ENCODER_PATH, 'r') as zipObj:
           zipObj.extractall()
        
        self.encoder = load_model(ENCODER)
        
        self.tfidf = load(TFIDF)
        
        self.encoded_dtm = load(ENCODED_DTM)
        
        # Fit on DTM
        self.nn = NearestNeighbors(n_neighbors=5, algorithm='kd_tree')
        self.nn.fit(self.encoded_dtm)
        
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
