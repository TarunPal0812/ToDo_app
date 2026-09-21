run-dev:
		APP_ENV=development uv run fastapi dev --port 9000

run-prod:
		APP_ENV=production uv run fastapi dev --port 9090