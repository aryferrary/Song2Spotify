import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from shazamio import Shazam
import asyncio

# Spotify API-Zugangsdaten
client_id = ''
client_secret = ''
redirect_uri = 'https://www.example.com/callback'
scope = 'playlist-modify-public playlist-modify-private'

# Spotify-Authentifizierung
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope
))

# Playlist-ID (copy den link und dann ende von url)
playlist_id = ''

# Fortschritt verfolgen, damit erneutes Verarbeiten zu vermieden wird
progress_file = "progress_log.txt"
processed_songs = set()

# Fortschritt laden, falls vorhanden
if os.path.exists(progress_file):
    with open(progress_file, "r") as f:
        processed_songs = set(f.read().splitlines())

async def recognize_and_add_song(audio_file_path):
    # Versuche, den Song-Titel und Künstler in paar Sekunden zu erkennen
    
    
    try:
        shazam = Shazam()
        song_info = await asyncio.wait_for(shazam.recognize(audio_file_path), timeout=5)
        
        # Falls gefunden suche auf spot
        if 'track' in song_info:
            title = song_info['track']['title']
            artist = song_info['track']['subtitle']
            query = f"{title} {artist}"
            print(f"Erkannter Song durch Shazam: {title} von {artist}")
        else:
            # Falls Shazam abkackt, nutze den Dateinamen
            query = os.path.splitext(os.path.basename(audio_file_path))[0]
            print(f"Shazam konnte '{query}' nicht erkennen. Verwende den Dateinamen für die Spotify-Suche.")
    
    except asyncio.TimeoutError:
        # Falls die Erkennung die Zeit überschreitet, verwende den Dateinamen für die Spotify-Suche
        query = os.path.splitext(os.path.basename(audio_file_path))[0]
        print(f"Timeout für '{audio_file_path}'. Verwende den Dateinamen '{query}' für die Spotify-Suche.")
    
    except Exception as e:
        # Abfangen des 'end of stream'-Fehlers, kp warum der auftaucht und überspringen der Datei
        if "end of stream" in str(e):
            print(f"Fehler 'end of stream' bei '{audio_file_path}': Datei möglicherweise unvollständig oder nicht unterstütztes Format. Datei wird übersprungen.")
            return
        else:
            print(f"Ein unerwarteter Fehler trat bei der Verarbeitung von '{audio_file_path}' auf: {e}")
            return

    # Spotify-Suche mit dem ermittelten Query
    results = sp.search(q=query, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_uri = track['uri']
        
        # Track zur Playlist adden
        sp.playlist_add_items(playlist_id, [track_uri])
        print(f"Der Song '{query}' wurde zur Playlist hinzugefügt: {track_uri}")
    else:
        print(f"'{query}' wurde in Spotify nicht gefunden und wird übersprungen.")

    # Fortschritt speichern
    processed_songs.add(audio_file_path)
    with open(progress_file, "a", encoding="utf-8") as f:
        f.write(audio_file_path + "\n")


async def process_songs_in_folder(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        # Überprüfen, ob die Datei eine Audiodatei ist und ob sie bereits verarbeitet wurde
        if file_name.lower().endswith('.mp3') and file_path not in processed_songs:
            print(f"Verarbeite Datei: {file_name}")
            await recognize_and_add_song(file_path)

# Pfad zum Ordner mit den songs
folder_path = r"G:/M/"

# Code ausführen
if __name__ == "__main__":
    asyncio.run(process_songs_in_folder(folder_path))
