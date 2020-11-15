from flask import Flask, session
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from typing import Union

import json
import os
import spotipy
import uuid

spotify_conn: Union[None, spotipy.client.Spotify] = None


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(64)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./.flask_session/"

caches_dir = "./.spotify_caches/"
if not os.path.exists(caches_dir):
    os.makedirs(caches_dir)


def session_cache_path():
    return f"{caches_dir}{session.get('uuid')}"


@app.route("/")
def index():
    if not session.get("uuid"):
        session["uuid"] = str(uuid.uuid4())
    establish_connection()

    return "Connection established."


def get_auth_info(credential_fn) -> dict:
    with open(credential_fn, "r") as f:
        spotify_credentials = json.load(f)

    return spotify_credentials


def establish_connection(credential_fn: str = "spotify_credentials.json"):
    global spotify_conn
    spotify_info: dict = get_auth_info(credential_fn)
    spotify_conn = Spotify(auth_manager=SpotifyOAuth(scope="user-read-currently-playing user-library-modify",
                                                     cache_path=session_cache_path(),
                                                     client_id=spotify_info["client_id"],
                                                     client_secret=spotify_info["client_secret"],
                                                     redirect_uri=spotify_info["redirect_uri"]))


@app.route("/like_currently_playing_song")
def like_currently_playing_song():
    global spotify_conn
    if spotify_conn is None:
        establish_connection()
    track_id = spotify_conn.current_user_playing_track()["item"]["id"]
    spotify_conn.current_user_saved_tracks_add([track_id])

    return "Liked!"


if __name__ == '__main__':
    app.run(port=5002)
