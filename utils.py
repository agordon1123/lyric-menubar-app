import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import requests
from bs4 import BeautifulSoup
from decouple import config
import re

username = config('SPOTIFY_USERNAME')
scope = config('SCOPE')
lyrics_base_url = config('LYRICS_BASE_URL')

def get_current_song():
    # authenticate
    try:
        token = util.prompt_for_user_token(username, scope)
    except (AttributeError, JSONDecodeError):
        os.remove(f'.cache-{username}')
        token = util.prompt_for_user_token(username, scope)
    # create spotify object
    spotifyObject = spotipy.Spotify(auth=token)
    # capture device being played on
    devices = spotifyObject.devices()
    # print(json.dumps(devices, sort_keys=True, indent=4))
    deviceId = devices['devices'][0]['id']
    # capture track information
    track = spotifyObject.current_user_playing_track()
    artist = track['item']['artists'][0]['name']
    track = track['item']['name']
    artist != '' and print('Currently playing ' + artist + ' - ' + track)
    # capture user information
    user = spotifyObject.current_user()
    displayName = user['display_name']
    follower = user['followers']['total']
    return (artist, track)

def get_lyrics(artist, song):
    # remove ^the and special characters
    re_the = r'^(the)'
    re_special = r'[^a-zA-Z0-9 \n\.]'
    artist = artist.lower().replace(' ', '')
    artist = re.sub(re_the, '', artist)
    artist = re.sub(re_special, '', artist)
    song = song.lower().replace(' ', '')
    # get html from lyric site
    response = requests.request('GET', f'{lyrics_base_url}/{artist}/{song}.html')
    content = BeautifulSoup(response.content, 'html.parser')
    # parse to remove unneeded content and format string
    lyrics = content.find_all('div', attrs={'class': 'row'})
    data_string = str(lyrics)
    start = data_string.find('that. -->') + len('that. -->')
    end = data_string.find('<!-- MxM')
    formatted_lyrics = data_string[start:end].replace('<br>', '').replace('<br/>', ' ').replace('</div>', '')
    return formatted_lyrics
