.PHONY:
run:
	ssh -t pi@raspberrypi.local "/usr/bin/python /home/pi/code/main.py"

.PHONY:
program:
	rsync ./*.py pi@raspberrypi.local:/home/pi/code

.PHONY:
load_music:
	rsync ./music/*.wav pi@raspberrypi.local:/home/pi/music

.PHONY:
shutdown_pi:
	ssh pi@raspberrypi.local "sudo shutdown now"
