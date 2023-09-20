#!/usr/bin/python3
import json
import unittest

from app.playlist_content import PlaylistContent


class TestPlaylistContent(unittest.TestCase):

    def test_can_parse_playlist_content(self):
        playlist_content_inst = PlaylistContent(name="2019", playlist_id="2Qu7CovYYekPQojJpr23VD")
        raw_playlist_content = read_json_content('test_data/example_playlist_content.json')
        playlist_content_inst.parse_playlist(raw_playlist_content)

        parsed_playlist_tracks = playlist_content_inst.tracks
        self.assertEqual(len(parsed_playlist_tracks), 13)

        first_entry = parsed_playlist_tracks[0]
        self.assertIn("spotify:track:3mnqWACBGfk2AO2eonicIT", first_entry.uri)
        self.assertIn("Hard Drive", first_entry.title)
        self.assertIn("Cassandra Jenkins", first_entry.artist.name)
        self.assertIn("1WVGbBnzZ5WLZ2PfesIHik", first_entry.artist.id)
        self.assertIn("An Overview on Phenomenal Nature",
                      first_entry.album.name)
        self.assertIn("0QURjDbfsPsDa5R4sgkjV9", first_entry.album.id)

    def test_empty_playlist_content_nothing_to_parse(self):
        playlist_content_inst = PlaylistContent(name="2019", playlist_id="2Qu7CovYYekPQojJpr23VD")
        raw_playlist_content = {"items": []}
        playlist_content_inst.parse_playlist(raw_playlist_content)
        parsed_playlist_tracks = playlist_content_inst.tracks
        self.assertEqual(len(parsed_playlist_tracks), 0)

    def test_can_parse_album_list(self):
        playlist_content_inst = PlaylistContent(name="Discover Weekly Albums")
        raw_playlist_content = read_json_content('test_data/example_album_list_content.json')
        playlist_content_inst.parse_album_list(raw_playlist_content)

        parsed_playlist_tracks = playlist_content_inst.tracks
        self.assertEqual(len(parsed_playlist_tracks), 275)

        first_entry = parsed_playlist_tracks[0]
        self.assertIn("spotify:track:6KgohznOqWD1tri8qkwgaD", first_entry.uri)
        self.assertIn("Soil", first_entry.title)
        self.assertIn("naomi paris tokyo", first_entry.artist.name)
        self.assertIn("42NNGTf3N5jtBfsYn6P3s8", first_entry.artist.id)
        self.assertIn("Soil", first_entry.album.name)
        self.assertIn("7iRPjbJfu9l6S6pWixab1X", first_entry.album.id)

    def test_empty_album_list_content_nothing_to_parse(self):
        playlist_content_inst = PlaylistContent(name="Discover Weekly Albums")
        raw_playlist_content = []
        playlist_content_inst.parse_album_list(raw_playlist_content)
        parsed_playlist_tracks = playlist_content_inst.tracks
        self.assertEqual(len(parsed_playlist_tracks), 0)

    def test_can_parse_genre_recommentation_content(self):
        playlist_content_inst = PlaylistContent(name="Ambient Recommendations")
        raw_genre_recommendation_content = read_json_content("test_data/example_genre_recommendation_content.json")
        playlist_content_inst.parse_playlist(raw_genre_recommendation_content)

        parsed_playlist_tracks = playlist_content_inst.tracks
        self.assertEqual(len(parsed_playlist_tracks), 30)

        first_entry = parsed_playlist_tracks[0]
        self.assertIn("spotify:track:2RQIQtothw4tp854k911cY", first_entry.uri)
        self.assertIn("Stokkseyri", first_entry.title)
        self.assertIn("Jónsi", first_entry.artist.name)
        self.assertIn("3khg8RDB6nMuw34w1IHS6Y", first_entry.artist.id)
        self.assertIn("Riceboy Sleeps", first_entry.album.name)
        self.assertIn("7geaPgu6PxeEyhBOa20ajZ", first_entry.album.id)


def read_json_content(filename):
    with open(filename) as json_file:
        return json.load(json_file)
