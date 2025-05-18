include .env
export $(shell sed 's/=.*//' .env)

# 開発環境に置けるコマンド
.PHONY: dev
dev:
	docker compose up -d --build

.PHONY: down
down:
	docker compose down

.PHONY: local-prod
local-prod:
	docker compose -f compose.prod.yaml up -d --build

.PHONY: local-prod-down
local-prod-down:
	docker compose -f compose.prod.yaml down

#  backend
.PHONY: ba
ba:
	docker compose exec backend bash

.PHONY: cb
cb:
	docker compose build

.PHONY: cu
cu:
	docker compose up


# ConohaVPSでDBを立てるときのコマンド
.PHONY: conoha-db
conoha-db:
	docker compose -f compose.db.yaml up -d

# GCPにDjangoをデプロイするときのコマンド
.PHONY: generate-env-yaml
generate-env-yaml:
	@echo "" > .env.yaml
	@grep -v -e '^PORT=' -e '^#' -e '^$$' .env | while IFS='=' read -r key val; do \
		cleaned_val=$$(echo $$val | sed 's/^"\(.*\)"$$/\1/'); \
		echo "$$key: \"$$cleaned_val\"" >> .env.yaml; \
	done

.PHONY gcp-build:
gcp-build:
	docker build -t asia-northeast1-docker.pkg.dev/$(PROJECT_ID)/$(REPOSITORY)/django-app -f ./docker/backend/Dockerfile.prod ./backend

.PHONY gcp-push:
gcp-push:
	docker push asia-northeast1-docker.pkg.dev/$(PROJECT_ID)/$(REPOSITORY)/django-app

.PHONY: gcp-deploy
gcp-deploy:
	gcloud run deploy django-app \
	--image asia-northeast1-docker.pkg.dev/$(PROJECT_ID)/$(REPOSITORY)/django-app \
	--region asia-northeast1 \
	--platform managed \
	--allow-unauthenticated \
	--max-instances=1 \
	--env-vars-file=.env.yaml

.PHONY: deploy
deploy:
	@echo "Deploying to GCP..."
	@make gcp-build
	@make gcp-push
	@make generate-env-yaml
	@make gcp-deploy
	@echo "Cleaning up..."
	@rm -f .env.yaml
	@echo "Deployment complete."