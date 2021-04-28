"""Machine learning functions"""
import logging
import random
from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator
import joblib
import pickle
from tfidf import df
from tfidf import dtm
from os.path import dirname
from tfidf import spotify_songs
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm.notebook import tqdm
DIR = dirname(__file__)
MODELS_DIR = DIR + '/../models/'

log = logging.getLogger(__name__)
router = APIRouter()

model_filename = MODELS_DIR + 'nlp_model.pkl'
loaded_model = pickle.load(open(model_filename, 'rb'))

class Item(BaseModel):
    """Use this data model to parse the request body JSON."""

    x1: float = Field(..., example=3.14)
    x2: int = Field(..., example=-42)
    x3: str = Field(..., example='banjo')

    def to_df(self):
        """Convert pydantic object to pandas dataframe with 1 row."""
        return pd.DataFrame([dict(self)])

    @validator('x1')
    def x1_must_be_positive(cls, value):
        """Validate that x1 is a positive number."""
        assert value > 0, f'x1 == {value}, must be > 0'
        return value


@router.post('/predict')
async def predict(artist, song):
    #translate artist, song into doc dtm.iloc[x].values
    artist_songs = df.loc[df['track_artist'] == artist]
    selected_song = artist_songs.loc[artist_songs['track_name'] == song]
    x = selected_song.index
    x= x[0]
    x = x.item()
    doc = dtm.loc[x].values
    result = loaded_model.kneighbors([doc], n_neighbors=6)

    rec_songs = {"artist": [], "song": []};

    for i in range(5):
        song = result[1][0][1 + i]

        # translate the loc into an artist and song title
        artist = df.loc[song]['track_artist']
        song = df.loc[song]['track_name']

        rec_songs['artist'].append(artist)
        rec_songs['song'].append(song)

    return rec_songs
