#!/usr/bin/python3

from flask import make_response, render_template

from app import app, cache
from app.playlist_service import PlaylistService

playlist_service = PlaylistService()


@app.route('/new-releases', methods=['GET'])
@cache.cached()
def get_new_releases():
    new_releases = playlist_service.get_new_releases()
    if len(new_releases.albums) == 0:
        return make_response({'message': 'No new releases at this time'}, 200)
    else:
        return render_template("new_releases.html", new_releases=new_releases)
