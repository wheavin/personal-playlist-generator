# /bin/bash

echo "Starting Personal Playlist Generator application"
source venv/bin/activate
pytest
flask --debug run -h localhost -p 8080
