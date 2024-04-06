"""
Complete audio system class that serves as middle
level of abstraction between IO and logic
"""

import os
import sys
import glob
from display import Display
from audio_player import AudioPlayer


class AudioSystem:
    def __init__(self, music_dir: str):
        # setting properties
        self.music_dir = music_dir

        # reading wav files in music directory
        self.music_files = glob.glob(os.path.join(self.music_dir, '*.wav'))
        if len(self.music_files) <= 0:
            print('Error: no valid music files in directory `%s`' % self.music_dir)
            sys.exit(-1)
        else:
            print('Loaded %d wav files:' % len(self.music_files))
            for i in range(len(self.music_files)):
                print('\t%d %s' % (i, self.music_files[i]))

        # initializing player and screen
        print('Initializing display')
        self.disp = Display()

        print('Initializing audio player')
        self.player = AudioPlayer()
        self.current_song = 0

        self.load_current_song()


    def load_current_song(self):
        # loading new song, starting player, updating display
        if self.player.playing:
            self.player.stop()
        self.player.load(self.music_files[self.current_song])
        self.update_disp()


    def update_disp(self):
        self.disp.write('%s %s' % (self.current_song, self.player.song_title))


    def play(self):
        if self.player.playing:
            print('Stopping player')
            self.player.stop()
        else:
            print('Starting player')
            self.player.play()

        self.update_disp()


    def prev(self):
        print('Selecting previous song')
        if self.current_song > 0:
            self.current_song -= 1
        else:
            self.current_song = len(self.music_files) - 1
        
        self.load_current_song()


    def next(self):
        print('Selecting next song')
        if self.current_song < len(self.music_files) - 1:
            self.current_song += 1
        else:
            self.current_song = 0

        self.load_current_song()
