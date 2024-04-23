PI_USER=pi
PI_HOST=raspberrypi.local
CODE_DIR=/home/$(PI_USER)/code
SRC_DIR=./src


.PHONY:
load_music:
	rsync ./music/*.wav $(PI_USER)@$(PI_HOST):/home/$(PI_USER)/music

.PHONY:
setup:
	rsync ./setup.sh $(PI_USER)@$(PI_HOST):/home/$(PI_USER)
	ssh -t $(PI_USER)@$(PI_HOST) "sudo chmod +x setup.sh; sudo ./setup.sh"

.PHONY:
program:
	# copy the code to the device
	rsync $(SRC_DIR)/*.py $(PI_USER)@$(PI_HOST):$(CODE_DIR)

.PHONY:
start: program
	# copy the service file
	rsync --rsync-path="sudo rsync" ./player.service $(PI_USER)@$(PI_HOST):/lib/systemd/system
	# start the systemctl service which runs the python code
	ssh -t $(PI_USER)@$(PI_HOST) "sudo chmod 644 /lib/systemd/system/player.service; sudo chmod +x $(CODE_DIR)/main.py; sudo systemctl daemon-reload; sudo systemctl enable player.service; sudo systemctl restart player.service"

.PHONY:
test: program
	# run the code in an interactive ssh shell
	ssh -t $(PI_USER)@$(PI_HOST) "/usr/bin/python $(CODE_DIR)/main.py"
 
.PHONY:
stop:
	# stopping the service
	ssh -t $(PI_USER)@$(PI_HOST) "sudo systemctl stop player.service"

.PHONY:
shutdown_pi:
	ssh $(PI_USER)@$(PI_HOST) "sudo shutdown now"

.PHONY:
clean:
	# cleans out the code and service file and disables service
	ssh -t $(PI_USER)@$(PI_HOST) "sudo systemctl stop player.service; sudo rm /lib/systemd/system/player.service; sudo rm -rf $(CODE_DIR)"
