import time
from flask import Flask, url_for, request, redirect, g, render_template
from markupsafe import escape
from queries import Query
import spotipy.util as util
import spotipy
import json
import requests
from urllib.parse import quote
from flask_cors import CORS, cross_origin
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
CORS(app, allow_headers="*")


@app.route("/search")
def foo():
    search = request.args.get("search")
    artist = request.args.get("artist")
    album = request.args.get("album")
    unique = request.args.get("unique") == "True"
    print("unique=", type(unique))

    query = Query(search, album, artist, unique)
    result = []
    if not query.q:
        return {"result": result}
    print("query=", query.q)
    query_result = query.make_query()
    query_result = list(map((lambda x: vars(x)), query_result))
    result.extend(query_result)
    #         offset += 50
    return {"result": result}


# Authentication Steps, paramaters, and responses are defined at https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response.


#  Client Keys
CLIENT_ID = "eff9cc476569450dae3888575a2f3d23"
CLIENT_SECRET = "87fa5e3e68574e7db27c15db25a52a8e"

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 5000
REDIRECT_URI = "http://127.0.0.1:5001/callback/q"
SCOPE = "playlist-modify-public playlist-modify-private playlist-read-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()
CACHE_PATH = "/home/sebvil/dev/src/git/playlist-manager/api/.cache"
auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID,
}


@app.route("/get_playlists")
def get_user_playlists():
    oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=CACHE_PATH,
    )
    print(oauth.scope)

    sp = spotipy.Spotify(oauth_manager=oauth)
    user = sp.current_user()["display_name"]
    offset = 0
    playlists = []
    while results := sp.current_user_playlists(offset=offset)["items"]:
        for playlist in results:
            print(playlist["name"])
            if playlist["owner"]["display_name"] == user:
                playlists.append(playlist)
        offset += 50

    return {"playlists": playlists}


@app.route("/check_login")
def check_login():
    oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=CACHE_PATH,
    )
    token = oauth.get_cached_token()

    if token:
        return {"logged_in": "true"}
    else:
        return {"logged_in": "false"}


@app.route("/login", methods=["POST", "GET", "OPTIONS"])
@cross_origin(allow_headers="*")
def login():
    oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=CACHE_PATH,
    )

    token = oauth.get_access_token()
    if token:
        return {"logged_in": "true"}
    else:
        return {"logged_in": "false"}


@app.route("/new/<name>/<visibility>")
def new_playlist(name=None, visibility=None):
    if not name or not visibility:
        return {"error": "no playlist name"}
    oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=CACHE_PATH,
    )
    print(oauth.scope)
    visibility = visibility == "public"

    token = oauth.get_access_token()
    if token:
        sp = spotipy.Spotify(oauth_manager=oauth)
        user = sp.current_user()["display_name"]
        sp.user_playlist_create(user, name, public=visibility)
        return {"success": "success"}
    else:
        return {"error": "could not authenticate"}


@app.route("/callback/q")
def callback():
    print(2)
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args["code"]
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    # Get profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(
        user_profile_api_endpoint, headers=authorization_header
    )
    profile_data = json.loads(profile_response.text)

    # Get user playlist data
    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    playlists_response = requests.get(
        playlist_api_endpoint, headers=authorization_header
    )
    playlist_data = json.loads(playlists_response.text)

    # Combine profile and playlist data to display
    display_arr = [profile_data] + playlist_data["items"]
    return {"login": "true"}


# if __name__ == "__main__":
#     app.run(debug=True, port=PORT)


@app.route("/add", methods=["POST"])
def add_to_playlists():
    if request.method == "POST":
        req = request.get_json()
        print(req)
        print(type(req))
        playlists = req["playlists"]
        tracks = req["tracks"]
        oauth = SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            cache_path=CACHE_PATH,
        )
        token = oauth.get_access_token()
        if token:
            sp = spotipy.Spotify(oauth_manager=oauth)

            for playlist in playlists:
                sp.user_playlist_add_tracks(
                    sp.current_user()["id"], playlist, tracks, position=None
                )


# Authentication Steps, paramaters, and responses are defined at https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response.


#  Client Keys
# CLIENT_ID = "eff9cc476569450dae3888575a2f3d23"
# CLIENT_SECRET = "3d2f89fcc6f54e9196f58f1f1ef80354"

# # Spotify URLS
# SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
# SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
# SPOTIFY_API_BASE_URL = "https://api.spotify.com"
# API_VERSION = "v1"
# SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# # Server-side Parameters
# CLIENT_SIDE_URL = "http://127.0.0.1"
# PORT = 5000
# REDIRECT_URI = "http://127.0.0.1:5001/callback/q"
# SCOPE = "playlist-modify-public playlist-modify-private playlist-read-private"
# STATE = ""
# SHOW_DIALOG_bool = True
# SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()
# CACHE_PATH = "/home/sebastian/Desktop/Projects/Personal/spotify_manager/playlist-manager/api/.cache"
# auth_query_parameters = {
#     "response_type": "code",
#     "redirect_uri": REDIRECT_URI,
#     "scope": SCOPE,
#     # "state": STATE,
#     # "show_dialog": SHOW_DIALOG_str,
#     "client_id": CLIENT_ID,
# }


# @app.route("/get_playlists")
# def get_user_playlists():
#     oauth = SpotifyOAuth(
#         client_id=CLIENT_ID,
#         client_secret=CLIENT_SECRET,
#         redirect_uri=REDIRECT_URI,
#         scope=SCOPE,
#         cache_path=CACHE_PATH,
#     )
#     print(oauth.scope)

#     sp = spotipy.Spotify(oauth_manager=oauth)
#     user = sp.current_user()["display_name"]
#     offset = 0
#     playlists = []
#     while results := sp.current_user_playlists(offset=offset)["items"]:
#         for playlist in results:
#             print(playlist["name"])
#             if playlist["owner"]["display_name"] == user:
#                 playlists.append(playlist)
#         offset += 50

#     return {"playlists": playlists}


# @app.route("/check_login")
# def check_login():
#     oauth = SpotifyOAuth(
#         client_id=CLIENT_ID,
#         client_secret=CLIENT_SECRET,
#         redirect_uri=REDIRECT_URI,
#         scope=SCOPE,
#         cache_path=CACHE_PATH,
#     )
#     token = oauth.get_cached_token()

#     if token:
#         return {"logged_in": "true"}
#     else:
#         return {"logged_in": "false"}


# @app.route("/login", methods=["POST", "GET", "OPTIONS"])
# @cross_origin(allow_headers="*")
# def login():
#     oauth = SpotifyOAuth(
#         client_id=CLIENT_ID,
#         client_secret=CLIENT_SECRET,
#         redirect_uri=REDIRECT_URI,
#         scope=SCOPE,
#         cache_path=CACHE_PATH,
#     )

#     token = oauth.get_access_token()
#     if token:
#         return {"logged_in": "true"}
#     else:
#         return {"logged_in": "false"}


# @app.route("/new/<name>/<visibility>")
# def new_playlist(name=None, visibility=None):
#     if not name or not visibility:
#         return {"error": "no playlist name"}
#     oauth = SpotifyOAuth(
#         client_id=CLIENT_ID,
#         client_secret=CLIENT_SECRET,
#         redirect_uri=REDIRECT_URI,
#         scope=SCOPE,
#         cache_path=CACHE_PATH,
#     )
#     print(oauth.scope)
#     visibility = visibility == "public"

#     token = oauth.get_access_token()
#     if token:
#         sp = spotipy.Spotify(oauth_manager=oauth)
#         user = sp.current_user()["display_name"]
#         sp.user_playlist_create(user, name, public=visibility)
#         return {"success": "success"}
#     else:
#         return {"error": "could not authenticate"}


# @app.route("/callback/q")
# def callback():
#     print(2)
#     # Auth Step 4: Requests refresh and access tokens
#     auth_token = request.args["code"]
#     code_payload = {
#         "grant_type": "authorization_code",
#         "code": str(auth_token),
#         "redirect_uri": REDIRECT_URI,
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET,
#     }
#     post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

#     # Auth Step 5: Tokens are Returned to Application
#     response_data = json.loads(post_request.text)
#     access_token = response_data["access_token"]
#     refresh_token = response_data["refresh_token"]
#     token_type = response_data["token_type"]
#     expires_in = response_data["expires_in"]

#     # Auth Step 6: Use the access token to access Spotify API
#     authorization_header = {"Authorization": "Bearer {}".format(access_token)}

#     # Get profile data
#     user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
#     profile_response = requests.get(
#         user_profile_api_endpoint, headers=authorization_header
#     )
#     profile_data = json.loads(profile_response.text)

#     # Get user playlist data
#     playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
#     playlists_response = requests.get(
#         playlist_api_endpoint, headers=authorization_header
#     )
#     playlist_data = json.loads(playlists_response.text)

#     # Combine profile and playlist data to display
#     display_arr = [profile_data] + playlist_data["items"]
#     return {"login": "true"}


# # if __name__ == "__main__":
# #     app.run(debug=True, port=PORT)


# @app.route("/add", methods=["POST"])
# def add_to_playlists():
#     if request.method == "POST":
#         req = request.get_json()
#         print(req)
#         print(type(req))
#         playlists = req["playlists"]
#         tracks = req["tracks"]
#         oauth = SpotifyOAuth(
#             client_id=CLIENT_ID,
#             client_secret=CLIENT_SECRET,
#             redirect_uri=REDIRECT_URI,
#             scope=SCOPE,
#             cache_path=CACHE_PATH,
#         )
#         token = oauth.get_access_token()
#         if token:
#             sp = spotipy.Spotify(oauth_manager=oauth)

#             for playlist in playlists:
#                 sp.user_playlist_add_tracks(
#                     sp.current_user()["id"], playlist, tracks, position=None
#                 )

#         return {"added": "SUCCESS"}
#     return {"added": "FAILURE"}


#
# @app.route('/login/<username>')
# def login(username):
#     scope = 'user-library-read'
#     if not username:
#         return {'error': 'login failed'}
#
#     token = util.prompt_for_user_token(username=username, scope=scope)
#
#     playlists_fn = []
#     if token:
#         sp = spotipy.Spotify(auth=token)
#         playlists = sp.user_playlists(username)
#         for playlist in playlists['items']:
#             if playlist['owner']['id'] == username:
#                 print()
#                 print(playlist['name'])
#                 playlists_fn.append(playlist)
#         return {'playlists' : playlists_fn}
#
