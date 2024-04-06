PI_USER=pi
PI_HOST=raspberrypi.local
CODE_DIR=/home/$(PI_USER)/code


.PHONY:
load_music:
	rsync ./music/*.wav $(PI_USER)@$(PI_HOST):/home/$(PI_USER)/music

.PHONY:
setup:
	rsync ./setup.sh $(PI_USER)@$(PI_HOST):/home/$(PI_USER)
	ssh -t $(PI_USER)@$(PI_HOST) "sudo chmod +x setup.sh; sudo ./setup.sh"

.PHONY:
program:
	# first copying the code
	rsync ./code/*.py ./player.service $(PI_USER)@$(PI_HOST):$(CODE_DIR)
	# then copy the service file and start the service
	ssh -t $(PI_USER)@$(PI_HOST) "sudo cp $(CODE_DIR)/player.service /lib/systemd/system; sudo chmod 644 /lib/systemd/system/player.service; sudo chmod +x $(CODE_DIR)/main.py; sudo systemctl daemon-reload; sudo systemctl enable player.service; sudo systemctl restart player.service"

.PHONY:
run:
	ssh -t $(PI_USER)@$(PI_HOST) "/usr/bin/python $(CODE_DIR)/main.py"

.PHONY:
shutdown_pi:
	ssh $(PI_USER)@$(PI_HOST) "sudo shutdown now"
