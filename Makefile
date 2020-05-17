.PHONY: server
server:
	uvicorn server.main:app --reload --port 8001
