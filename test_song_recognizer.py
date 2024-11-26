import shazamio
from shazamio import Shazam

async def recognize_song(audio_file):
    shazam = Shazam()
    song_info = await shazam.recognize(audio_file)
    return song_info

# Anwendungsbeispiel
import asyncio
song = asyncio.run(recognize_song(r"G:\M\05 - Greeky-05-greeky.mp3"))
print(song)




