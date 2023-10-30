#!/usr/bin/python3

import json

from app.domain.music_domain import Artist, Album, Track


class Playlist:

    def __init__(self, name, playlist_id) -> None:
        self.name = name
        self.id = playlist_id


class PlaylistContent:
    def __init__(self, name="", playlist_id="") -> None:
        self.name = name
        self.id = playlist_id
        self.tracks = []

    @staticmethod
    def empty():
        return PlaylistContent()

    def parse_playlist(self, playlist_content):
        playlist_items = self.get_playlist_items(playlist_content)
        playlist_tracks = []
        for playlist_item in playlist_items:
            if 'track' in playlist_item:
                playlist_track = playlist_item['track']
            else:
                playlist_track = playlist_item
            title = playlist_track['name']
            uri = playlist_track['uri']
            artist = self._parse_artist(playlist_track)
            album = self._parse_album(playlist_track)
            playlist_tracks.append(Track(title=title, uri=uri, artist=artist, album=album))
        self.tracks = playlist_tracks

    @staticmethod
    def get_playlist_items(playlist_content):
        if 'items' in playlist_content:
            return playlist_content['items']
        elif 'tracks' in playlist_content:
            return playlist_content['tracks']
        return []

    def parse_album_list(self, album_list):
        playlist_tracks = []
        for album_item in album_list:
            album = Album(name=album_item['name'], album_id=album_item['id'])
            album_tracks = album_item['tracks']['items']
            for track_item in album_tracks:
                track_artist = track_item['artists'][0]
                artist = Artist(name=track_artist['name'], artist_id=track_artist['id'])
                track_title = track_item['name']
                track_uri = track_item['uri']
                playlist_tracks.append(Track(title=track_title, uri=track_uri, artist=artist, album=album))
        self.tracks = playlist_tracks

    @staticmethod
    def _parse_artist(playlist_track):
        track_artist = playlist_track['artists'][0]
        return Artist(name=track_artist['name'], artist_id=track_artist['id'])

    @staticmethod
    def _parse_album(playlist_track):
        track_album = playlist_track['album']
        return Album(name=track_album['name'], album_id=track_album['id'])

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
