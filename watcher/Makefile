.PHONY: fmt
fmt:
	python3 -m black .

.PHONY: start-watcher
start-watcher:
	python3 watcher.py

.PHONY: start-api
start-api:
	python3 -m uvicorn api:app
