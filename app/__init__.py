from flask import Flask
from flask_caching import Cache

app = Flask(__name__)
cache = Cache()
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
app.config['CACHE_KEY_PREFIX'] = 'playgen_'
cache.init_app(app)

from app import playlists, recommendations, new_releases
