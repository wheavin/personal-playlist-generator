#!/usr/bin/python3

from unittest.mock import patch

from spotipy import Spotify, SpotifyException

from app.tests.test_base import TestBase, read_json_content
from playlist_generator import app

HEADERS = {'Content-Type': 'multipart/form-data'}


class TestRecommendations(TestBase):

    @patch.object(Spotify, 'recommendation_genre_seeds')
    def test_get_recommendation_genre_seeds_returns_multiple_items(self, mock_recommendation_genre_seeds):
        mock_recommendation_genre_seeds.return_value = read_json_content(
            "test_data/example_genre_seed_content.json")
        with app.test_client() as http_client:
            response = http_client.get('/recommendations-genre')
            self.assertEqual(200, response.status_code)
            self.assertIn(b"deep-house", response.data, msg="Response data should contain genre name")
            # call again to test genre seed cache
            response = http_client.get('/recommendations-genre')
            self.assertEqual(200, response.status_code)
            self.assertIn(b"electronic", response.data, msg="Response data should contain genre name")

    @patch.object(Spotify, 'recommendation_genre_seeds')
    def test_get_recommendation_genre_seeds_returns_empty(self, mock_recommendation_genre_seeds):
        mock_recommendation_genre_seeds.return_value = {"genres": []}
        with app.test_client() as http_client:
            response = http_client.get('/recommendations-genre')
            self.assertEqual(200, response.status_code)

    @patch.object(Spotify, 'recommendation_genre_seeds')
    def test_get_recommendation_genre_seeds_throws_exception(self, mock_recommendation_genre_seeds):
        mock_recommendation_genre_seeds.side_effect = SpotifyException(500, 1, "Error getting genre seeds")
        with app.test_client() as http_client:
            response = http_client.get('/recommendations-genre')
            self.assertEqual(200, response.status_code)

    @patch.object(Spotify, 'recommendations')
    def test_get_recommendations_for_genre(self, mock_recommendations):
        mock_recommendations.return_value = read_json_content(
            "test_data/fake_genre_recommendations.json")
        form_data = {'genre': 'metal'}
        with app.test_client() as http_client:
            response = http_client.post('recommendations-genre-items', headers=HEADERS, data=form_data)
            self.assertEqual(200, response.status_code)
            self.assertIn(b"Cool Album Name", response.data)
            self.assertIn(b"Cool Band Name", response.data)
            self.assertIn(b"Cool Song", response.data)

    @patch.object(Spotify, 'recommendations')
    def test_get_recommendations_for_genre_no_input_data(self, mock_recommendations):
        with app.test_client() as http_client:
            response = http_client.post('recommendations-genre-items', headers=HEADERS, data={})
            self.assertEqual(200, response.status_code)
            mock_recommendations.assert_not_called()

    @patch.object(Spotify, 'recommendations')
    def test_get_recommendations_for_genre_throws_exception(self, mock_recommendations):
        mock_recommendations.side_effect = SpotifyException(500, 1, "Error getting genre recommendations")
        form_data = {'genre': 'metal'}
        with app.test_client() as http_client:
            response = http_client.post('recommendations-genre-items', headers=HEADERS, data=form_data)
            self.assertEqual(200, response.status_code)
