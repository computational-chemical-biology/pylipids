build:
	docker build -t pylipids .

bash:
	docker run -it -p 5020:5020 --rm -v $(shell pwd):/home/pylipids --name pylipids pylipids bash

interactive:
	docker run -it -p 5020:5020 --rm -v $(shell pwd):/home/pylipids --name pylipids pylipids sh /home/pylipids/run_server.sh

server:
	docker run -itd -p 5020:5020 --rm -v $(shell pwd):/home/pylipids --name pylipids pylipids sh /home/pylipids/run_server.sh
