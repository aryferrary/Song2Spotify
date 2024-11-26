import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API-Zugangsdaten
client_id = ''
client_secret = ''
redirect_uri = 'https://www.example.com/callback'
scope = 'playlist-modify-public playlist-modify-private'

# Spotify-Authentifizierung einrichten
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    show_dialog=True
))

# Playlist-ID
playlist_id = ''

def remove_duplicates_from_playlist(playlist_id):
    # Abrufen aller Tracks in der Playlist
    playlist_tracks = []
    results = sp.playlist_items(playlist_id)
    playlist_tracks.extend(results['items'])
    
    # Falls es mehr als 100 Tracks gibt, alle Seiten abrufen
    while results['next']:
        results = sp.next(results)
        playlist_tracks.extend(results['items'])
    
    # Track-URIs sammeln und Duplikate identifizieren
    track_uris = {}
    duplicate_track_uris = []

    for idx, item in enumerate(playlist_tracks):
        track_uri = item['track']['uri']
        if track_uri in track_uris:
            # Wenn der Track-URI bereits existiert, ist es ein Duplikat
            duplicate_track_uris.append({'uri': track_uri, 'positions': [idx]})
        else:
            # Den Track in die Liste der eindeutigen Tracks hinzufügen und die Position speichern
            track_uris[track_uri] = idx

    # Entferne die Duplikate in Batches von 100, behalte die erste Instanz
    if duplicate_track_uris:
        for i in range(0, len(duplicate_track_uris), 100):
            batch = duplicate_track_uris[i:i + 100]
            sp.playlist_remove_specific_occurrences_of_items(
                playlist_id,
                [{'uri': item['uri'], 'positions': item['positions']} for item in batch]
            )
        print(f"Duplikate erfolgreich entfernt: {len(duplicate_track_uris)} Songs")
    else:
        print("Keine Duplikate gefunden.")

# Duplikate aus der Playlist entfernen
remove_duplicates_from_playlist(playlist_id)
