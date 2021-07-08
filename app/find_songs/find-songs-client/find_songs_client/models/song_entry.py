from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SongEntry")


@attr.s(auto_attribs=True)
class SongEntry:
    """ """

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
    genres: str
    lang: str
    lyrics: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        popularity = self.popularity
        duration_ms = self.duration_ms
        explicit = self.explicit
        artists = self.artists
        id_artists = self.id_artists
        release_date = self.release_date
        danceability = self.danceability
        energy = self.energy
        key = self.key
        loudness = self.loudness
        mode = self.mode
        speechiness = self.speechiness
        acousticness = self.acousticness
        instrumentalness = self.instrumentalness
        liveness = self.liveness
        valence = self.valence
        tempo = self.tempo
        time_signature = self.time_signature
        genres = self.genres
        lang = self.lang
        lyrics = self.lyrics

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "popularity": popularity,
                "duration_ms": duration_ms,
                "explicit": explicit,
                "artists": artists,
                "id_artists": id_artists,
                "release_date": release_date,
                "danceability": danceability,
                "energy": energy,
                "key": key,
                "loudness": loudness,
                "mode": mode,
                "speechiness": speechiness,
                "acousticness": acousticness,
                "instrumentalness": instrumentalness,
                "liveness": liveness,
                "valence": valence,
                "tempo": tempo,
                "time_signature": time_signature,
                "genres": genres,
                "lang": lang,
            }
        )
        if lyrics is not UNSET:
            field_dict["lyrics"] = lyrics

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        popularity = d.pop("popularity")

        duration_ms = d.pop("duration_ms")

        explicit = d.pop("explicit")

        artists = d.pop("artists")

        id_artists = d.pop("id_artists")

        release_date = d.pop("release_date")

        danceability = d.pop("danceability")

        energy = d.pop("energy")

        key = d.pop("key")

        loudness = d.pop("loudness")

        mode = d.pop("mode")

        speechiness = d.pop("speechiness")

        acousticness = d.pop("acousticness")

        instrumentalness = d.pop("instrumentalness")

        liveness = d.pop("liveness")

        valence = d.pop("valence")

        tempo = d.pop("tempo")

        time_signature = d.pop("time_signature")

        genres = d.pop("genres")

        lang = d.pop("lang")

        lyrics = d.pop("lyrics", UNSET)

        song_entry = cls(
            id=id,
            name=name,
            popularity=popularity,
            duration_ms=duration_ms,
            explicit=explicit,
            artists=artists,
            id_artists=id_artists,
            release_date=release_date,
            danceability=danceability,
            energy=energy,
            key=key,
            loudness=loudness,
            mode=mode,
            speechiness=speechiness,
            acousticness=acousticness,
            instrumentalness=instrumentalness,
            liveness=liveness,
            valence=valence,
            tempo=tempo,
            time_signature=time_signature,
            genres=genres,
            lang=lang,
            lyrics=lyrics,
        )

        song_entry.additional_properties = d
        return song_entry

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
