#!/usr/bin/python3
import json
import unittest
from unittest import mock

from playlist_generator import app


def read_json_content(filename):
    with open(filename) as json_file:
        return json.load(json_file)


class TestBase(unittest.TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        mock_token = mock.patch('SpotifyOAuth.get_access_token')
        mock_token.return_value = "fake_token"
