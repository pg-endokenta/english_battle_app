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