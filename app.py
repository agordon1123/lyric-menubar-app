import rumps
import os
import subprocess
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

# from decouple import config
# username = config('SPOTIFY_USERNAME')
# scope = config('SCOPE')
# cientId = config('SPOTIFY_CLIENT_ID')
# secretKey = config('SPOTIFY_CLIENT_SECRET')

class LyricApp:
    def __init__(self):
        self.config = {
            'app_name': 'Lyrical',
        }
        self.app = rumps.App(self.config['app_name'], '🎧')
        
    def run(self):
        self.app.run()

    def get_current_song(self):
        # authenticate
        try:
            token = util.prompt_for_user_token(SPOTIFY_USERNAME, SCOPE)
        except (AttributeError, JSONDecodeError):
            os.remove(f'.cache-{SPOTIFY_USERNAME}')
            token = util.prompt_for_user_token(SPOTIFY_USERNAME, SCOPE)
        # create spotify object
        spotifyObject = spotipy.Spotify(auth=token)
        # capture device being played on
        devices = spotifyObject.devices()
        # print(json.dumps(devices, sort_keys=True, indent=4))
        deviceId = devices['devices'][0]['id']
        # capture track information
        track = spotifyObject.current_user_playing_track()
        # print(json.dumps(track, sort_keys=True, indent=4))
        # print()
        artist = track['item']['artists'][0]['name']
        track = track['item']['name']
        artist != "" and print('Currently playing ' + artist + ' - ' + track)
        # capture user information
        user = spotifyObject.current_user()
        displayName = user['display_name']
        follower = user['followers']['total']
    
    def get_OS_info(self):
        f = os.popen('ps aux')
        target = ''
        for line in f:
            if 'SpotMenu' in line:
                target = line
        print("!!", target)
    
if __name__ == '__main__':
    app = LyricApp()
    # app.run()
    app.get_current_song()