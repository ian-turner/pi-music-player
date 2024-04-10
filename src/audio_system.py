"""
Complete audio system class that serves as middle
level of abstraction between IO and logic
"""

import os
import sys
import glob
from time import time, sleep
from display import Display
from audio_player import AudioPlayer
from gpiozero import LED
import subprocess


DISPLAY_REFRESH_RATE = 50
ON_LED_PIN = 12


class AudioSystem:
    def __init__(self, music_dir: str):
        # initializing display module
        print('Initializing display output')
        self.disp = Display()

        # initializing audio player module
        print('Initializing audio player')
        self.player = AudioPlayer()

        # reading music from directory
        self.load_music_dir(music_dir)

        # setting current song
        self.load_song(0)


    def update_display(self):
        # writing the song title
        self.disp.message = self.player.song_title

        # setting track number
        self.disp.current_song = self.current_song

        # setting time indicator
        if self.player.playing:
            self.disp.time_sec = int(time() - self.player.start_time + self.player.song_pos)
        else:
            self.disp.time_sec = int(self.player.song_pos)
        self.disp.playing = self.player.playing
        self.disp.song_time_sec = self.player.song_time_sec

        self.disp.update()
        sleep(DISPLAY_REFRESH_RATE / 1000)


    def load_music_dir(self, music_dir: str):
        # reading wav files in music directory
        self.music_files = glob.glob(os.path.join(music_dir, '*.wav'))
        self.num_songs = len(self.music_files)
        if self.num_songs <= 0:
            print('Error: no valid music files in directory `%s`' % self.music_dir)
            sys.exit(-1)
        else:
            print('Loaded %d wav files:' % len(self.music_files))
            for i in range(self.num_songs):
                print('\t%d %s' % (i, self.music_files[i]))


    def load_song(self, idx: int):
        # stopping player if it's already playing
        if self.player.playing:
            self.player.stop()

        # loading new song, starting player, updating display
        self.current_song = idx
        self.player.load(self.music_files[self.current_song])

    def play(self):
        if self.player.playing:
            print('Stopping player')
            self.player.stop()
        else:
            print('Starting player')
            self.player.play()


    def prev(self):
        print('Selecting previous song')
        if self.current_song > 0:
            self.load_song(self.current_song - 1)
        else:
            self.load_song(self.num_songs - 1)


    def next(self):
        print('Selecting next song')
        if self.current_song < self.num_songs - 1:
            self.load_song(self.current_song + 1)
        else:
            self.load_song(0)


    def shutdown(self):
        print('Shutting down audio system')
        # stopping audio playback
        self.player.stop()

        # shutting off display
        self.disp.close()

        # shutting down OS
        subprocess.call(['sudo', 'shutdown', '-h', 'now'], shell=False)
