build:
	docker build -t complex .

bash:
	docker run -it -p 5000:5000 --rm -v $(shell pwd):/home/complex --name complex complex bash

interactive:
	docker run -it -p 5000:5000 --rm -v $(shell pwd):/home/complex --name complex complex sh /home/complex/run_server.sh

server:
	docker run -itd -p 5000:5000 --rm -v $(shell pwd):/home/complex --name complex complex sh /home/complex/run_server.sh
