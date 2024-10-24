#!/usr/bin/python3

from flask import render_template, request, make_response
from spotipy import SpotifyException

from app import app, cache
from app.playlist_service import PlaylistService

playlist_service = PlaylistService()


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/all-playlists', methods=['GET'])
@cache.cached()
def get_all_playlists():
    try:
        playlists = playlist_service.get_all_playlists()
        if playlists:
            return render_template("playlists.html", playlists=playlists)
        else:
            return render_template("playlist_notification.html", page_title="My Playlists",
                                   info_message="Hmmmm. Looks like you have no playlists yet.")
    except SpotifyException as ex:
        error_message = "Error occurred when getting all playlists. {}".format(ex)
        print(error_message)
        return render_template("playlist_notification.html", page_title="My Playlists",
                               info_message="Oops! Looks like we cannot fetch your playlists right now :(")


@app.route('/playlist', methods=['GET'])
@cache.cached()
def get_playlist():
    playlist_name, playlist_content = _get_playlist_content()
    if playlist_content and playlist_content.tracks:
        return render_template("playlist_tracks.html", playlist_content=playlist_content)
    else:
        info_message = "Playlist is empty" if playlist_content else "Playlist not found"
        return render_template("playlist_notification.html", page_title=playlist_name, info_message=info_message)


@app.route('/playlist-albums', methods=['GET'])
@cache.cached()
def get_albums_for_playlist_tracks():
    """
    Returns a playlist comprised of the albums of the provided tracks.
    :return:
    """
    playlist_name, playlist_content = _get_playlist_content()
    if playlist_content and playlist_content.tracks:
        album_ids = [track.album.id for track in playlist_content.tracks]
        album_content = playlist_service.get_albums_playlist(album_ids=album_ids, playlist_name=playlist_name)
        return render_template("playlist_tracks.html", playlist_content=album_content)
    else:
        info_message = "Playlist is empty" if playlist_content else "Playlist not found"
        return render_template("playlist_notification.html", page_title=playlist_name, info_message=info_message)


def _get_playlist_content():
    playlist_id = request.args.get("id")
    playlist_name = request.args.get("name")
    playlist_content = playlist_service.get_playlist(playlist_id=playlist_id, playlist_name=playlist_name)
    return playlist_name, playlist_content


@app.route('/playlist', methods=['POST'])
def create_playlist():
    """
    Creates a new playlist using the provided playlist name and tracks.
    :return: 200 OK response if playlist successfully created
    """
    try:
        json_data = request.get_json()
        playlist_name = json_data['name']
        playlist_tracks = json_data['tracks']
        tracks_to_add = [track['uri'] for track in playlist_tracks]
    except KeyError:
        error_message = "Invalid playlist input"
        print(error_message)
        return make_response({'message': error_message, 'code': 'FAILURE'}, 400)

    if not playlist_name:
        return make_response({'message': 'Playlist name must be provided', 'code': 'FAILURE'}, 400)

    try:
        print("Creating playlist -", playlist_name)
        playlist_service.create_playlist(playlist_name=playlist_name, tracks_to_add=tracks_to_add)
        return make_response({'message': 'Playlist successfully created', 'code': 'SUCCESS'}, 200)
    except SpotifyException as ex:
        error_message = "Error occurred when creating playlist. {}".format(ex)
        print(error_message)
        return make_response({'message': error_message, 'code': 'SUCCESS'}, 500)
