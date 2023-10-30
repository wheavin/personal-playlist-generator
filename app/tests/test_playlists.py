#!/usr/bin/python3

import json
from unittest.mock import patch

from spotipy import Spotify, SpotifyException

from app.tests.test_base import TestBase, read_json_content
from playlist_generator import app

HEADERS = {'Content-Type': 'application/json'}


class TestPlaylists(TestBase):

    @patch.object(Spotify, 'current_user_playlists')
    def test_get_all_playlists_returns_multiple_items(self, mock_playlists):
        mock_playlists.return_value = {
            "items": [{"name": "Playlist 1", "id": "1234"}, {"name": "Playlist 2", "id": "5678"}]}
        with app.test_client() as http_client:
            response = http_client.get('/all-playlists')
            self.assertEqual(200, response.status_code)
            self.assertIn(b"Playlist 1", response.data)
            self.assertIn(b"Playlist 2", response.data)

    @patch.object(Spotify, 'current_user_playlists')
    def test_get_all_playlists_returns_large_number(self, mock_playlists):
        mock_playlists.side_effect = [
            read_json_content("test_data/fake_playlist_data_1.json"),
            read_json_content("test_data/fake_playlist_data_2.json"),
            read_json_content("test_data/fake_playlist_data_3.json"),
        ]
        with app.test_client() as http_client:
            response = http_client.get('/all-playlists')
            self.assertEqual(200, response.status_code)
            self.assertIn(b"Playlist 1", response.data)
            self.assertIn(b"Playlist 51", response.data)
            self.assertIn(b"Playlist 101", response.data)
            self.assertIn(b"Playlist 125", response.data)

    @patch.object(Spotify, 'current_user_playlists')
    def test_get_all_playlists_returns_empty(self, mock_playlists):
        mock_playlists.return_value = {"items": []}
        with app.test_client() as client:
            response = client.get('/all-playlists')
            self.assertEqual(200, response.status_code)
            self.assertIn(b"My Playlists", response.data)
            self.assertIn(b"Hmmmm. Looks like you have no playlists yet.", response.data)

    @patch.object(Spotify, 'current_user_playlists')
    def test_get_all_playlists_throws_exception(self, mock_playlists):
        mock_playlists.side_effect = SpotifyException(400, -1, "Bad request for url")
        with app.test_client() as client:
            response = client.get('/all-playlists')
            self.assertEqual(200, response.status_code)
            self.assertIn(b"My Playlists", response.data)
            self.assertIn(b"Oops! Looks like we cannot fetch your playlists right now :(", response.data)

    @patch.object(Spotify, 'playlist_items')
    def test_get_playlist_by_id(self, mock_playlist):
        mock_playlist.return_value = read_json_content('test_data/fake_playlist_track.json')

        with app.test_client() as http_client:
            response = http_client.get('/playlist?id=hfh8y7934y93y&name=Cool+Playlist')
            self.assertEqual(200, response.status_code)
            self.assertIn(b"Cool Playlist", response.data, msg="Response data should contains playlist name")
            self.assertIn(b"Cool Album Name", response.data, msg="Response data should contain album name")
            self.assertIn(b"Cool Band Name", response.data, msg="Response data should contain artist name")
            self.assertIn(b"Cool Song", response.data, msg="Response data should contain song name")
            self.assertIn(b"spotify:artist:hfh8y7934y93y", response.data, msg="Response data should contain song uri")
            mock_playlist.assert_called_with(playlist_id='hfh8y7934y93y')

    @patch.object(Spotify, 'playlist_items')
    def test_get_playlist_by_id_empty(self, mock_playlist):
        mock_playlist.return_value = {"items": []}

        with app.test_client() as http_client:
            response = http_client.get('/playlist?id=hfh8y7934y93y')
            self.assertEqual(200, response.status_code)
            self.assertIn(b"Playlist is empty", response.data)

    @patch.object(Spotify, 'playlist_items')
    @patch.object(Spotify, 'current_user_playlists')
    def test_get_playlist_by_name(self, mock_playlists, mock_playlist):
        mock_playlists.return_value = {
            "items": [{"name": "Playlist 1", "id": "1234"}, {"name": "Playlist 2", "id": "5678"}]}
        mock_playlist.return_value = read_json_content('test_data/fake_playlist_track.json')

        with app.test_client() as http_client:
            response = http_client.get('/playlist?name=Playlist+1')
            self.assertEqual(200, response.status_code)
            self.assertIn(b"Playlist 1", response.data, msg="Response data should contains playlist name")
            self.assertIn(b"Cool Album Name", response.data, msg="Response data should contain album name")
            self.assertIn(b"Cool Band Name", response.data, msg="Response data should contain artist name")
            self.assertIn(b"Cool Song", response.data, msg="Response data should contain song name")
            self.assertIn(b"spotify:artist:hfh8y7934y93y", response.data, msg="Response data should contain song uri")
            mock_playlist.assert_called_with(playlist_id='1234')

    @patch.object(Spotify, 'playlist_items')
    @patch.object(Spotify, 'current_user_playlists')
    def test_get_playlist_by_name_not_found(self, mock_playlists, mock_playlist):
        mock_playlists.return_value = {
            "items": [{"name": "Playlist 1", "id": "1234"}, {"name": "Playlist 2", "id": "5678"}]}
        mock_playlist.return_value = read_json_content('test_data/fake_playlist_track.json')

        with app.test_client() as http_client:
            response = http_client.get('/playlist?name=Playlist+3')
            self.assertEqual(200, response.status_code)
            self.assertIn(b"Playlist not found", response.data)

    @patch.object(Spotify, 'playlist_add_items')
    @patch.object(Spotify, 'user_playlist_create')
    def test_create_small_playlist(self, mock_playlist_create, mock_playlist_add_items):
        mock_playlist_create.return_value = {"id": "6dynHw32vMmVGCxQKU5FaI"}

        playlist_data = json.dumps({"name": "Playlist 1", "tracks": [
            {"uri": "spotify:track:1"},
            {"uri": "spotify:track:2"},
            {"uri": "spotify:track:3"},
            {"uri": "spotify:track:4"},
            {"uri": "spotify:track:5"}
        ]})
        with app.test_client() as http_client:
            response = http_client.post('/playlist', headers=HEADERS, data=playlist_data)
            self.assertEqual(200, response.status_code)
            self.assertIn(b"Playlist successfully created", response.data)
        mock_playlist_add_items.assert_called_once()

    @patch.object(Spotify, 'playlist_add_items')
    @patch.object(Spotify, 'user_playlist_create')
    def test_create_large_playlist(self, mock_playlist_create, mock_playlist_add_items):
        mock_playlist_create.return_value = {"id": "6dynHw32vMmVGCxQKU5FaI"}

        playlist_data = json.dumps(read_json_content('test_data/fake_track_list.json'))
        with app.test_client() as http_client:
            response = http_client.post('/playlist', headers=HEADERS, data=playlist_data)
            self.assertEqual(200, response.status_code)
            self.assertIn(b"Playlist successfully created", response.data)
        self.assertEqual(mock_playlist_add_items.call_count, 2)

    @patch.object(Spotify, 'playlist_add_items')
    @patch.object(Spotify, 'user_playlist_create')
    def test_create_empty_playlist(self, mock_playlist_create, mock_playlist_add_items):
        mock_playlist_create.return_value = {"id": "6dynHw32vMmVGCxQKU5FaI"}

        playlist_data = json.dumps({"name": "Playlist 1", "tracks": []})
        with app.test_client() as http_client:
            response = http_client.post('/playlist', headers=HEADERS, data=playlist_data)
            self.assertEqual(200, response.status_code)
            self.assertIn(b"Playlist successfully created", response.data)
        mock_playlist_add_items.assert_not_called()

    @patch.object(Spotify, 'playlist_add_items')
    @patch.object(Spotify, 'user_playlist_create')
    def test_create_playlist_no_name(self, mock_playlist_create, mock_playlist_add_items):
        playlist_data = json.dumps({"name": None, "tracks": []})
        with app.test_client() as http_client:
            response = http_client.post('/playlist', headers=HEADERS, data=playlist_data)
            self.assertEqual(400, response.status_code)
            self.assertIn(b"Playlist name must be provided", response.data)
        mock_playlist_create.assert_not_called()
        mock_playlist_add_items.assert_not_called()
