"""
Class that handles loading and playing audio files asynchronously
using subprocess spawning and multithreading
"""

import os
from time import time, sleep
from subprocess import Popen, PIPE
from threading import Thread


# refresh rate in milliseconds
DEFAULT_REFRESH_RATE = 50


class AudioPlayer:
    def __init__(self, refresh_rate: int = DEFAULT_REFRESH_RATE):
        self.song_file = None
        self.sub_proc = None
        self.time_msec = 0
        self.counter_thread = None
        self.playing = False
        self.refresh_rate = refresh_rate
        self.song_title = ''


    def load(self, file: str):
        # clear settings and load new audio file
        self.song_file = file
        self.time_msec = 0
        self.sub_proc = None
        self.playing = False
        self.song_title = os.path.basename(self.song_file).split('.')[0]


    def step_time(self):
        # infinite loop until song is paused
        while self.playing:
            self.time_msec += self.refresh_rate
            sleep(self.refresh_rate / 1000)


    def play(self):
        self.playing = True
        # recovering timestamp from previous play
        timestamp = '%.2f' % (self.time_msec / 1000)

        # starting a subprocess to play the audio with sox
        self.sub_proc = Popen(['play', self.song_file, 'trim', timestamp],
                              stdin=PIPE, stdout=PIPE, stderr=PIPE)
        print('Starting song at %ss' % timestamp)

        # starting thread to count how long song has been playing
        self.counter_thread = Thread(target=self.step_time)
        self.counter_thread.start()


    def stop(self):
        # stops the counting thread and updates state
        if self.playing:
            # stopping the audio playback
            self.sub_proc.kill()
            self.playing = False
