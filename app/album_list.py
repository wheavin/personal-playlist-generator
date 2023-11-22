#!/usr/bin/python3
import json

from app.domain.music_domain import Album


class AlbumList:

    def __init__(self, album_content_json=None):
        if album_content_json is None or len(album_content_json) == 0:
            self.albums = []
        else:
            self.albums = self._parse_album_content(album_content_json)

    @staticmethod
    def of(album_content_json):
        return AlbumList(album_content_json)

    @staticmethod
    def empty():
        return AlbumList()

    @staticmethod
    def _parse_album_content(album_content_json):
        albums = []
        album_items = album_content_json['albums']['items']
        for album in album_items:
            album_name = album['name']
            album_uri = album['uri']
            album_artist = album['artists'][0]
            album_artist_name = album_artist['name']
            albums.append(Album(name=album_name, album_uri=album_uri, artist=album_artist_name))
        return albums

    def add(self, album_content_json):
        if album_content_json is None or len(album_content_json) <= 0:
            return 0
        albums_parsed = self._parse_album_content(album_content_json)
        self.albums.extend(albums_parsed)
        return len(albums_parsed)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
