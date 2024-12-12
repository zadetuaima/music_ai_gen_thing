import spotipy
import os
import json
import re
import requests
from spotipy.oauth2 import SpotifyOAuth
from sclib import SoundcloudAPI, Track, Playlist
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
import yt_dlp

# Helper functions
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

with open("key.json", "r") as file:
    api_tokens = json.load(file)

client_secret = api_tokens['client_secret']
client_id = api_tokens['client_id']
redirectURI = api_tokens['redirect']

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirectURI,
                                               scope="playlist-read-private"))

# SoundCloud setup
with open("soundcloud_key.json", "r") as sound_file:
    sound_api_tokens = json.load(sound_file)

sound_id = sound_api_tokens['client_id']
sound_api = SoundcloudAPI(client_id=sound_id)

# Path to save downloads
download_path = r'C:\Users\Zade\Downloads\Test'







def download_from_youtube(query, download_path):
    """Downloads audio from YouTube based on the query."""
    sanitized_query = sanitize_filename(query)
    mp3_file_path = os.path.join(download_path, f"{sanitized_query}.mp3")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',  # <------------------------- Change Spotify download quality
            },
        ],
        'outtmpl': os.path.join(download_path, f"{sanitized_query}.%(ext)s"),
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([f"ytsearch:{query}"])
        except Exception as e:
            print('YT search failed line 63')


def download_spotify_playlist(track_url):
    """Downloads a single Spotify track."""
    try:
        track_id = track_url.split("/")[-1].split("?")[0]
        track = sp.track(track_id)
        track_name = sanitize_filename(f"{track['artists'][0]['name']} - {track['name']}")
        download_from_youtube(track_name, download_path)
        file_path = os.path.join(download_path, f"{track_name}.mp3")
        print(f"Downloaded Spotify track: {track_name}")
    except Exception as e:
        print(f"Error downloading Spotify track: {e}")

# SoundCloud download logic
def download_soundcloud_playlist(url):
    """Downloads a single SoundCloud track."""
    try:
        track = sound_api.resolve(url)
        if isinstance(track, Track):
            track_name = sanitize_filename(f"{track.artist} - {track.title}.mp3")
            file_path = os.path.join(download_path, track_name)
            with open(file_path, 'wb+') as file:
                track.write_mp3_to(file)
            print(f"Track downloaded! {track_name}")
        else:
            print("Provided URL is not a valid track.")
    except Exception as e:
        print(f"Error downloading SoundCloud track: {e}")
