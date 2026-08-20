.PHONY: youtube-auth youtube-reauthorize youtube-analytics-sync youtube-analytics-sync-full youtube-analytics-report youtube-channel-test x-auth x-test x-analytics-sync instagram-import-token instagram-test instagram-analytics-sync social-analytics-test analytics-dashboard dashboard-up dashboard-down

DASHBOARD_PORT := 8765
DASHBOARD_URL := http://127.0.0.1:$(DASHBOARD_PORT)/
DASHBOARD_PID_FILE := /tmp/dlatwd-analytics-dashboard.pid
DASHBOARD_LOG_FILE := /tmp/dlatwd-analytics-dashboard.log

youtube-auth:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/youtube-channel youtube-channel auth

youtube-reauthorize:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/youtube-channel youtube-channel auth --force

youtube-analytics-sync:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/youtube-channel youtube-channel sync

youtube-analytics-sync-full:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/youtube-channel youtube-channel sync --full

youtube-analytics-report:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/youtube-channel youtube-channel report

youtube-channel-test:
	PYTHONPATH=tools/youtube-channel/src tools/youtube-channel/.venv/bin/python -m unittest discover -s tools/youtube-channel/tests -v

x-auth:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/social-analytics social-analytics x-auth

x-test:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/social-analytics social-analytics x-test

x-analytics-sync:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/social-analytics social-analytics x-sync

instagram-import-token:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/social-analytics social-analytics instagram-import-token

instagram-test:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/social-analytics social-analytics instagram-test

instagram-analytics-sync:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/social-analytics social-analytics instagram-sync

social-analytics-test:
	PYTHONPATH=tools/social-analytics/src python3 -m unittest discover -s tools/social-analytics/tests -v

analytics-dashboard:
	python3 tools/analytics-dashboard/dashboard.py

# Background variant of analytics-dashboard: starts the server detached,
# waits for it to answer, and opens it in the default browser. Use
# `make dashboard-down` to stop it. Prefer `analytics-dashboard` when you
# want a foreground process you can Ctrl+C.
dashboard-up:
	@if [ -f $(DASHBOARD_PID_FILE) ] && kill -0 "$$(cat $(DASHBOARD_PID_FILE))" 2>/dev/null; then \
		echo "Dashboard already running (PID $$(cat $(DASHBOARD_PID_FILE))) at $(DASHBOARD_URL)"; \
	else \
		nohup python3 tools/analytics-dashboard/dashboard.py > $(DASHBOARD_LOG_FILE) 2>&1 & \
		echo $$! > $(DASHBOARD_PID_FILE); \
		for i in 1 2 3 4 5 6 7 8 9 10; do \
			curl -s -o /dev/null "$(DASHBOARD_URL)" && break; \
			sleep 0.5; \
		done; \
		echo "Dashboard running (PID $$(cat $(DASHBOARD_PID_FILE))) at $(DASHBOARD_URL)"; \
	fi
	@open $(DASHBOARD_URL) 2>/dev/null || true

dashboard-down:
	@if [ -f $(DASHBOARD_PID_FILE) ] && kill -0 "$$(cat $(DASHBOARD_PID_FILE))" 2>/dev/null; then \
		kill "$$(cat $(DASHBOARD_PID_FILE))" && echo "Stopped dashboard (PID $$(cat $(DASHBOARD_PID_FILE)))"; \
	else \
		echo "Dashboard is not running (or was not started with dashboard-up)"; \
	fi
	@rm -f $(DASHBOARD_PID_FILE)
