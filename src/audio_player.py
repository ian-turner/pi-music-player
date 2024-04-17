"""
Class that handles loading and playing audio
files asynchronously using subprocess spawning
"""

import os
from time import time, sleep
import subprocess
from subprocess import Popen, PIPE


class AudioPlayer:
    def __init__(self):
        self.song_file = None
        self.sub_proc = None
        self.playing = False
        self.song_title = ''
        self.song_pos = 0
        self.start_time = 0
        self.song_time_sec = 1


    def load(self, file: str):
        # clear settings and load new audio file
        self.song_file = file
        self.song_pos = 0
        self.sub_proc = None
        self.playing = False
        self.song_title = os.path.basename(self.song_file).split('.')[0]
        self.get_song_length()


    def play(self):
        self.playing = True
        # recovering timestamp from previous play
        timestamp = '%.3f' % self.song_pos

        # starting a subprocess to play the audio with sox
        self.sub_proc = Popen(['play', self.song_file, 'trim', timestamp],
                              stdin=PIPE, stdout=PIPE, stderr=PIPE)
        self.start_time = time()
        print('Started \'%s\' at %.2fs' % (self.song_title, self.song_pos))


    def stop(self):
        # stops the audio playing thread and saves state
        if self.playing:
            # stopping the audio playback
            self.sub_proc.kill()
            self.playing = False
            
            # checking time to see how long it played for
            self.song_pos += time() - self.start_time
            print('Stopped \'%s\' at %.2fs' % (self.song_title, self.song_pos))

    
    def get_song_length(self):
        # getting song length using soxi
        self.song_time_sec = float(subprocess.run(['soxi', '-D', self.song_file], capture_output=True).stdout)
