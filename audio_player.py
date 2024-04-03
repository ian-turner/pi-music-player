"""
Class that handles loading and playing audio files asynchronously
using subprocess spawning and multithreading
"""

from time import time, sleep
from subprocess import Popen, PIPE
from threading import Thread


# refresh rate in milliseconds
DEFAULT_REFRESH_RATE = 50


class AudioPlayer:
    def __init__(self, refresh_rate: int = DEFAULT_REFRESH_RATE):
        self.sound_file = None
        self.sub_proc = None
        self.time_msec = 0
        self.counter_thread = None
        self.playing = False
        self.refresh_rate = refresh_rate


    def load(self, file: str):
        # clear settings and load new audio file
        self.sound_file = file
        self.time_msec = 0
        self.sub_proc = None
        self.playing = False


    def step_time(self):
        # infinite loop until song is paused
        while self.playing:
            self.time_msec += self.refresh_rate
            sleep(self.refresh_rate / 1000.)


    def play(self):
        self.playing = True
        # recovering timestamp from previous play
        timestamp = '%.2f' % (self.time_msec / 1000)

        # starting a subprocess to play the audio with sox
        self.sub_proc = Popen(['play', self.sound_file, 'trim', timestamp],
                              stdin=PIPE, stdout=PIPE, stderr=PIPE)

        # starting thread to count how long song has been playing
        self.counter_thread = Thread(target=self.step_time)
        self.counter_thread.start()


    def pause(self):
        # stops the counting thread and updates state
        self.playing = False

        # stopping the audio playback
        self.sub_proc.kill()
