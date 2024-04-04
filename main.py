from gpiozero import Button
from audio_player import AudioPlayer


if __name__ == '__main__':
    button = Button(21)
    last_val = 0
    player = AudioPlayer()
    player.load('song1.wav')

    while True:
        val = button.value
        if val == 1 and last_val == 0:
            print('button pressed')
            if player.playing:
                print('pausing player')
                player.pause()
            else:
                print('starting player')
                player.play()
        last_val = val
