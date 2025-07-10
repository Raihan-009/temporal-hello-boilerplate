worker-image:=temporal-worker
tag:=1.13
worker-container:=temporal-worker

build-worker:
	@ docker build -f worker/Dockerfile -t ${worker-image}:v${tag} .

run-worker:
	@ docker run --name ${worker-container} ${worker-image}:v${tag}

clean:
	@ docker stop ${worker-container}
	@ docker rm ${worker-container}

up:
	@ docker compose up --build -d

down:
	@ docker compose down -v

