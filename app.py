from rumps import *
from utils import *
import os
import sys

class LyricApp:
    def __init__(self):
        self.config = {
            'app_name': 'Lyrical',
        }
        self.app = rumps.App(self.config['app_name'], '🎧')
        rumps.debug_mode(True)
        
    def run(self):
        self.app.run()

    @clicked('Lyrics')
    def button(self):
        current = get_current_song()
        artist = current[0]
        song = current[1]
        default_text = f'{artist} - {song}'
        lyrics = get_lyrics(artist, song)
        Window(lyrics, title=default_text, dimensions=(0,0)).run()

    def get_OS_info(self):
        f = os.popen('ps aux')
        target = ''
        for line in f:
            if 'SpotMenu' in line:
                target = line
        print("!!", target)
    
if __name__ == '__main__':
    app = LyricApp()
    app.run()