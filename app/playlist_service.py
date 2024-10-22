#!/usr/bin/python3

from spotipy import SpotifyException

from app.album_list import AlbumList
from app.config.properties_reader import PropertiesReader
from app.playlist_content import Playlist, PlaylistContent
from app.spotify_client import SpotifyClient
from utils.files import get_full_path

ALBUMS_MAX_LIMIT = 20
TRACKS_MAX_LIMIT = 100
ITEMS_MAX_LIMIT = 50
NEW_RELEASES_MAX_LIMIT = 200
APP_CONFIG_FILE_PATH = "app/config/app-config.properties"


def batch(iterable, batch_size=1):
    iter_size = len(iterable)
    for index in range(0, iter_size, batch_size):
        yield iterable[index:min(index + batch_size, iter_size)]


class PlaylistService(object):

    def __init__(self):
        app_config_file = get_full_path(APP_CONFIG_FILE_PATH)
        properties_reader = PropertiesReader(app_config_file)
        self.username = properties_reader.get("USERNAME")
        self.spotify_client = SpotifyClient.get_instance()

    def get_playlist(self, playlist_id, playlist_name):
        if playlist_id is None:
            return self.get_playlist_content_by_name(playlist_name=playlist_name)
        else:
            return self.get_playlist_content(playlist_id=playlist_id, playlist_name=playlist_name)

    def get_all_playlists(self):
        all_playlist_items = []
        offset = 0
        while True:
            playlists_data = self.spotify_client.current_user_playlists(offset=offset)
            playlist_items = playlists_data["items"]
            all_playlist_items.extend(playlist_items)
            if len(playlist_items) >= ITEMS_MAX_LIMIT:
                offset += ITEMS_MAX_LIMIT
            else:
                break

        playlists = []
        for playlist_item in all_playlist_items:
            playlist = Playlist(name=playlist_item["name"], playlist_id=playlist_item["id"])
            playlists.append(playlist)
        return sorted(playlists, key=lambda playlist: playlist.name.lower())

    def get_playlist_content_by_name(self, playlist_name):
        all_playlists = self.get_all_playlists()
        playlist_matched = self._match_playlist(playlist_name, all_playlists)
        if playlist_matched:
            return self.get_playlist_content(playlist_id=playlist_matched.id, playlist_name=playlist_name)
        else:
            return None

    @staticmethod
    def _match_playlist(playlist_name, playlists):
        return next((playlist for playlist in playlists if playlist.name == playlist_name), None)

    def get_playlist_content(self, playlist_id, playlist_name):
        playlist_data_json = self.spotify_client.playlist_items(playlist_id=playlist_id)
        playlist_content = PlaylistContent(name=playlist_name, playlist_id=playlist_id)
        playlist_content.parse_playlist(playlist_data_json)
        return playlist_content

    def create_playlist(self, playlist_name, tracks_to_add):
        new_playlist = self.spotify_client.user_playlist_create(user=self.username, name=playlist_name)
        for tracks_chunk in batch(tracks_to_add, TRACKS_MAX_LIMIT):
            self.spotify_client.playlist_add_items(playlist_id=new_playlist['id'], items=tracks_chunk)

    def get_albums_playlist(self, album_ids, playlist_name):
        album_list_json = []
        for album_id_chunk in batch(album_ids, ALBUMS_MAX_LIMIT):
            albums_json = self.spotify_client.albums(album_id_chunk)
            album_list_json.extend(albums_json['albums'])

        playlist_content = PlaylistContent(name=playlist_name)
        playlist_content.parse_album_list(album_list_json)
        return playlist_content

    def get_recommendation_genre_seeds(self):
        try:
            genre_seed_json = self.spotify_client.recommendation_genre_seeds()
            return genre_seed_json['genres']
        except SpotifyException as ex:
            print(f"Error occurred getting genre seeds: {ex}")
            return []

    def get_recommendations_for_genre(self, genre_name):
        if not genre_name:
            return PlaylistContent.empty()
        playlist_content = PlaylistContent(name="Recommendations for genre: " + genre_name)
        try:
            recommendations_for_genre_json = self.spotify_client.recommendations(seed_genres=[genre_name], limit=30)
            playlist_content.parse_playlist(recommendations_for_genre_json)
        except SpotifyException as ex:
            print(f"Error occurred getting genre recommendations: {ex}")
        return playlist_content

    def get_new_releases(self):
        try:
            new_releases = AlbumList()
            offset = 0
            while len(new_releases.albums) < NEW_RELEASES_MAX_LIMIT:
                new_releases_json = self.spotify_client.new_releases(limit=ITEMS_MAX_LIMIT, offset=offset)
                releases_added_count = new_releases.add(new_releases_json)
                if releases_added_count == 0:
                    break
                offset += ITEMS_MAX_LIMIT
            return new_releases
        except SpotifyException as ex:
            print(f"Error occurred getting new releases: {ex}")
            return AlbumList.empty()
