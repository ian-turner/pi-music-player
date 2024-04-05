PI_USER=pi
PI_HOST=raspberrypi.local
CODE_DIR=/home/$(PI_USER)/code


.PHONY:
load_music:
	rsync ./music/*.wav $(PI_USER)@$(PI_HOST):/home/$(PI_USER)/music

.PHONY:
program:
	rsync ./*.py $(PI_USER)@$(PI_HOST):$(CODE_DIR)

.PHONY:
run:
	ssh -t $(PI_USER)@$(PI_HOST) "/usr/bin/python $(CODE_DIR)"

.PHONY:
shutdown_pi:
	ssh $(PI_USER)@$(PI_HOST) "sudo shutdown now"
