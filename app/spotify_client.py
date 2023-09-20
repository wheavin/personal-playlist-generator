#!/usr/bin/python3

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from app.config.properties_reader import PropertiesReader
from utils.files import get_full_path

REDIRECT_URI = "http://localhost:5000/callback"
CLIENT_SCOPES = "playlist-modify-public,playlist-read-private"
APP_CONFIG_FILE_PATH = "app/config/app-config.properties"


class SpotifyClient(object):
    _instance = None

    def __init__(self) -> None:
        app_config_file = get_full_path(APP_CONFIG_FILE_PATH)
        properties_reader = PropertiesReader(app_config_file)
        client_id = properties_reader.get("CLIENT_ID")
        client_secret = properties_reader.get("CLIENT_SECRET")
        SpotifyClient._instance = Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                                    client_secret=client_secret,
                                                                    redirect_uri=REDIRECT_URI,
                                                                    scope=CLIENT_SCOPES))

    @staticmethod
    def get_instance() -> Spotify:
        if SpotifyClient._instance is None:
            SpotifyClient()
        return SpotifyClient._instance
