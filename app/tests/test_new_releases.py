#!/usr/bin/python3

import unittest
from unittest.mock import patch

from spotipy import Spotify, SpotifyException

from app.tests.test_base import TestBase, read_json_content
from playlist_generator import app


class TestNewReleases(TestBase):

    @patch.object(Spotify, 'new_releases')
    def test_get_new_releases(self, mock_new_releases):
        mock_new_releases.return_value = read_json_content("test_data/example_new_releases_content.json")
        with app.test_client() as http_client:
            response = http_client.get('/new-releases')
            self.assertEqual(200, response.status_code)
            self.assertIn(b"James Blake", response.data, msg="Response should contain artist name")
            self.assertIn(b"Playing Robots Into Heaven", response.data, msg="Response should contain album name")
            # self.assertIn(b"spotify:album:2ZwNcWl8h9blysDE8i4juL", response.data,
            #               msg="Response should contain album uri") TODO: add later

    @patch.object(Spotify, 'new_releases')
    def test_get_new_releases_returns_empty(self, mock_new_releases):
        mock_new_releases.return_value = {}
        with app.test_client() as http_client:
            response = http_client.get('/new-releases')
            self.assertEqual(200, response.status_code)
            self.assertIn(b'No new releases at this time', response.data)

    @patch.object(Spotify, 'new_releases')
    def test_get_new_releases_throws_exception(self, mock_new_releases):
        mock_new_releases.side_effect = SpotifyException(500, 1, "Error getting new releases")
        with app.test_client() as http_client:
            response = http_client.get('/new-releases')
            self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
