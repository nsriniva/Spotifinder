from os import getenv
import logging
import uvicorn

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from fastapi.requests import Request
from fastapi import APIRouter
from requests import get

from .data_model.find_songs import FindSongEntries, FindSongRecommendations

from typing import Any, Optional

from pydantic import BaseModel


class SongEntry(BaseModel):
    id: str
    name: str
    popularity: int
    duration_ms: int
    explicit: int
    artists: str
    id_artists: str
    release_date: str
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    time_signature: int
    lyrics: Any
    genres: str
    lang: str

# global variables and services
router = APIRouter()
log = logging.getLogger(__name__)

REC_COLS = ['artist','song']
FEATURES = ['name', 'artists']
SPOTIFINDER = 'Spotifinder'


findSongEntries = FindSongEntries()
findSongRecommendations = FindSongRecommendations()

app = FastAPI(
    title="Find Songs",
    description="A RESTful API for the Spotifinder Project",
    version="0.1",
    docs_url="/"
)

@app.post('/matching_songs')
async def find_matching_songs(hint:str):
    return findSongEntries.find_matching_songs(hint)

@app.post('/recommended_songs')
async def get_recommmended_songs(song:SongEntry):
    return findSongRecommendations.get_recommended_songs_json(song.json())

if __name__ == '__main__':
    uvicorn.run(app, debug=True)
