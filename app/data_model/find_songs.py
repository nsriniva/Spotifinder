'''
Contains the implementation of the FindSongs class.
'''
from re import compile as rcompile
from zipfile import ZipFile
from os.path import dirname
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.neighbors import NearestNeighbors
from joblib import load

DIR = dirname(__file__)

rex = rcompile('[^a-zA-Z 0-9]')

tokenize = lambda x: rex.sub('', x.lower().replace(',', ' ').replace('-', ' '))

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

class FindSongs():
    '''
    This class implements 3 methods:
    (1) find_song_entries - Given a song suggestion string containing 
    partial/whole song name
    and/or artist, returns a dataframe of possible matches
    (2) find_song_entry - Given a song suggestion string returns either 
    a dataframe of possible matches(if the best_choice kw argument is 
    False) or a single entry(if the best_choice argumen is True - this 
    is the default value)
    (3) get_recommendations - Given a song entry returns a dataframe of 
    songs that are similar.
    '''
    def __init__(self):

        # Extract encoder.h5 from encoder.h5.zip
        with ZipFile(ENCODER_PATH, 'r') as zipObj:
            zipObj.extractall()

        # Load the model saved in ../../models/encoder.h5
        self.encoder = load_model(ENCODER)
        # Load the TfIDF vectorizer saved in tfidf.pkl
        self.tfidf = load(TFIDF)
        # Load the encoded DTM saved in encoded_dtm.pkl
        self.encoded_dtm = load(ENCODED_DTM)
        # Fit NearestNeighbors on encoded DTM
        self.nn = NearestNeighbors(n_neighbors=7, algorithm='ball_tree')
        self.nn.fit(self.encoded_dtm)

        # Numerical features associated with a song entry
        self.features = [
            'popularity', 'duration_ms', 'explicit', 'danceability',
            'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence',
            'tempo', 'time_signature'
        ]
        # Load the model saved in fg_encoder.h5
        self.fg_encoder = load_model(FG_ENCODER_PATH)
        # Load the TfIDF vectorizer for genres data saved in genres_tfidf.pkl
        self.genres_tfidf = load(GENRES_TFIDF)
        # The original DF is DTM generated by genres_tfidf from genres data
        # in the dataset + Numerical features
        # Load the encoded DF from fg_encoded_df.pkl
        self.fg_encoded_df = load(FG_ENCODED_DF)
        # Load the StandardScaler saved at scaler.pkl
        self.scaler = load(SCALER)

        # Fit NearestNeighbors on encoded DF
        self.fg_nn = NearestNeighbors(n_neighbors=7, algorithm='ball_tree')
        self.fg_nn.fit(self.fg_encoded_df)

        # Load tracks_df from zipped csv file tracks_genres_lyrics_en.csv.zip
        self.tracks_df = pd.read_csv(TRACKS)

        # Get rid of superfluous columns and rows
        self.tracks_df.drop(columns=['Unnamed: 0'], inplace=True)
        self.tracks_df = self.tracks_df[self.tracks_df.genres.isna() == False]

    def find_song_entries(self, sugg_str):
        '''
        Given sugg_str(a string containing part/whole of the
        song's name and/or artist) returns a dataframe of
        song entries that are the closest matches.
        '''

        # Vectorize the sugg_str by running it through tfidf
        vec = self.tfidf.transform([tokenize(sugg_str)]).todense()
        # Reduce dimensionality by running through encoder
        encoded_vec = self.encoder.predict(vec)
        # Get list of indices of entries that are closest to sugg_str
        entries = self.nn.kneighbors(encoded_vec)[1][0].tolist()
        # Get the list of indices of closest matches sorted in descending
        # order of popularity i.e. the first entry will have the highest
        # popularity value
        entries = self.tracks_df.iloc[entries].popularity.\
            sort_values(ascending=False).index.tolist()

        # Return a dataframe containing the entries
        return self.tracks_df.loc[entries]

    def find_song_entry(self, sugg_str, best_choice=True):
        '''
        Given sugg_str(a string containing part/whole of the
        song's name and/or artist) returns either a dataframe of
        song entries that are the closest matches(best_choice=False)
        or a single song entry(best_choice=True)
        '''


        # Get dataframe of song entries that are closest match
        # to sugg_str which is a string containing part/whole
        # of the song's name and/or artist.
        df = self.find_song_entries(sugg_str)

        # Convert sugg_str to a set of tokens
        sugg_set = set(tokenize(sugg_str).split())

        # Get the list of index values for the dataframe
        choice = df.index.tolist()

        if best_choice:
            # The caller wants just one entry for the best match

            # Given index value of a song entry row, returns a set of
            # tokens from the combined name and artists columns.
            # The array syntax ['name'] is used in place of the dot
            # syntax .name because .name returns the value from the index
            # column
            name_artists = lambda x: set(tokenize(df.loc[x]['name']+' '+
                                                  df.loc[x].artists).split())

            # Given a set of tokens, it returns the length of its
            # intersection with the sugg_set
            # This is used as a measure how similar the input is to the
            # sugg_set - the larger the return value, the greater the
            # similarity
            score_func = lambda x: len(sugg_set.intersection(x))

            choices = [(y, name_artists(y)) for y in choice]
            best_idx = 0
            best_score = score_func(choices[0][1])
            for idx, nm_art in enumerate(choices[1:]):
                score = score_func(nm_art[1])
                #print(f'{nm_art[1]}/{choices[best_idx][1]}/{sugg_set}::{score}/{best_score}')
                if score > best_score:
                    best_score = score
                    best_idx = idx+1

            choice = choices[best_idx][0]

        return df.loc[choice]

    def get_recommendations(self, x):
        '''
        Given a song entry x, returns a dataframe of similar songs.

        The similarity is determined based on the numerical 
        features(detailed in self.features) along with genres feature.
        '''
        # Convert the genres feature to a vector
        gvec = self.genres_tfidf.transform([tokenize(x.genres)]).todense()
        # Standardize the numerical features
        fvec = self.scaler.transform([x[self.features]])
        # Combine bot vectors to create a single features vector
        vec = [fvec.tolist()[0] + gvec.tolist()[0]]
        # Perform dimensionality reduction by running through fg_encoder
        encoded_vec = self.fg_encoder.predict(vec)
        # Get the list of indices of entries that are closest to
        # the input entry
        entries = self.fg_nn.kneighbors(encoded_vec)[1][0].tolist()
        # Sort the list of indices in descending order of popularity
        #entries = self.tracks_df.iloc[entries].popularity.\
        #    sort_values(ascending=False).index.tolist()

        # Return a dataframe containing the sorted list of entries.
        return self.tracks_df.iloc[entries]
