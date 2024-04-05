from time import sleep
from gpiozero import Button
from audio_system import AudioSystem


MUSIC_FOLDER = '/home/pi/music'
PLAY_BUTTON_PIN = 21
LEFT_BUTTON_PIN = 20
RIGHT_BUTTON_PIN = 16


if __name__ == '__main__':
    # initializing audio system abstraction
    system = AudioSystem(MUSIC_FOLDER)

    # setting up GPIO
    play_button = Button(PLAY_BUTTON_PIN)
    left_button = Button(LEFT_BUTTON_PIN)
    right_button = Button(RIGHT_BUTTON_PIN)

    # connecting buttons to system
    play_button.when_pressed = system.play
    left_button.when_pressed = system.prev
    right_button.when_pressed = system.next

    while True:
        sleep(1)
