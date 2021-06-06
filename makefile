APP_NAME=app001

start:
	export DOCKER_BUILDKIT=1
	export COMPOSE_DOCKER_CLI_BUILD=1
	docker-compose up --build -d
	echo Webpage avalible on localhost:9980
stop:
	docker-compose down -v --rmi all --remove-orphans
	echo Stoping and Cleaning finished
rebuild:
	docker-compose up -d --no-deps --build app
	echo Webserver rebuild with new data
