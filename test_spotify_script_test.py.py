import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify-Zugangsdaten
client_id = ''
client_secret = ''
redirect_uri = 'https://www.example.com/callback'
scope = 'playlist-modify-public playlist-modify-private'
# Authentifizierung
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    show_dialog=True
))
# Playlist-ID und Track-URI
playlist_id = ''
track_uri = 'spotify:track:4zxaoHZn5FwX00pm8zWcKO'

# Hinzufügen des Tracks zur Playlist
sp.playlist_add_items(playlist_id, [track_uri])




