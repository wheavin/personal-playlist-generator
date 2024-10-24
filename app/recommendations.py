#!/usr/bin/python3

from flask import render_template, request

from app import app, cache
from app.playlist_content import PlaylistContent
from app.playlist_service import PlaylistService

playlist_service = PlaylistService()

cached_genre_seeds = []


@app.route('/recommendations-genre', methods=['GET'])
@cache.cached()
def get_recommendation_genre_seeds():
    if not cached_genre_seeds:
        genre_seeds = playlist_service.get_recommendation_genre_seeds()
        cached_genre_seeds.extend(genre_seeds)
    return render_template("recommendations_for_genre.html", genres=cached_genre_seeds,
                           playlist_content=PlaylistContent.empty())


@app.route('/recommendations-genre-items', methods=['POST'])
def get_recommendations_for_genre():
    genre_name = request.form.get("genre")
    recommendations = playlist_service.get_recommendations_for_genre(genre_name=genre_name)
    return render_template("recommendations_for_genre.html", genres=cached_genre_seeds,
                           playlist_content=recommendations)
