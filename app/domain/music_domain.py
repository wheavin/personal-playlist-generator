#!/usr/bin/python3

import json


class Artist:

    def __init__(self, name, artist_id) -> None:
        self.name = name
        self.id = artist_id


class Album:

    def __init__(self, name, album_id="", album_uri="", artist="") -> None:
        self.name = name
        self.id = album_id
        self.uri = album_uri
        self.artist = artist


class Track:

    def __init__(self, title, uri, artist, album) -> None:
        self.uri = uri
        self.title = title
        self.artist = artist
        self.album = album

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
