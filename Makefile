IMAGE_NAME=whisper-transcribe-bot

.PHONY: build run shell push

prod-build-start:
	docker compose -f infra/docker/docker-compose.yml --env-file=configs/.env up --build -d

prod-start:
	docker compose -f infra/docker/docker-compose.yml --env-file=configs/.env up

prod-down:
	docker compose -f infra/docker/docker-compose.yml --env-file=configs/.env down v


dockerfile-only-build:
	docker build -f infra/docker/Dockerfile -t $(IMAGE_NAME) .

dockerfile-only-run:
	docker run --rm -it --env-file=configs/.env $(IMAGE_NAME)

dockerfile-only-run-shell:
	docker run --rm -it --env-file=configs/.env $(IMAGE_NAME) /bin/bash
