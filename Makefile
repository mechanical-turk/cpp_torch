.PHONY: analytics-sync youtube-auth youtube-reauthorize youtube-analytics-sync youtube-analytics-sync-full youtube-analytics-report youtube-captions-download youtube-video-chapters youtube-video-description-plain youtube-channel-test x-auth x-test x-audience-sync x-post-analytics-sync x-analytics-sync github-stars-sync instagram-import-token instagram-test instagram-analytics-sync tiktok-auth tiktok-test tiktok-analytics-sync tiktok-public-audience-sync social-analytics-test phyllo-sync phyllo-tiktok-sync phyllo-test analytics-dashboard dashboard-up dashboard-down

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

youtube-captions-download:
	@test -n "$(VIDEO_ID)" || (echo "VIDEO_ID is required" && exit 2)
	@test -n "$(OUTPUT)" || (echo "OUTPUT is required" && exit 2)
	UV_CACHE_DIR=build/uv-cache uv run --project tools/youtube-channel youtube-channel captions-download --video-id "$(VIDEO_ID)" --output "$(OUTPUT)"

youtube-video-chapters:
	@test -n "$(VIDEO_ID)" || (echo "VIDEO_ID is required" && exit 2)
	@test -n "$(CHAPTERS)" || (echo "CHAPTERS is required" && exit 2)
	UV_CACHE_DIR=build/uv-cache uv run --project tools/youtube-channel youtube-channel video-chapters --video-id "$(VIDEO_ID)" --file "$(CHAPTERS)" $(if $(APPLY),--apply,)

youtube-video-description-plain:
	@test -n "$(VIDEO_ID)" || (echo "VIDEO_ID is required" && exit 2)
	UV_CACHE_DIR=build/uv-cache uv run --project tools/youtube-channel youtube-channel video-description-plain --video-id "$(VIDEO_ID)" $(if $(APPLY),--apply,)

youtube-channel-test:
	PYTHONPATH=tools/youtube-channel/src tools/youtube-channel/.venv/bin/python -m unittest discover -s tools/youtube-channel/tests -v

x-auth:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/social-analytics social-analytics x-auth

x-test:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/social-analytics social-analytics x-test

x-audience-sync:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/social-analytics social-analytics x-audience-sync

# Tweet-level X metadata can consume API credits. Run this only when explicitly
# requested; it is deliberately excluded from the default dashboard refresh.
x-post-analytics-sync:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/social-analytics social-analytics x-sync

x-analytics-sync:
	@echo "Use 'make x-audience-sync' for the routine follower refresh."
	@echo "Use 'make x-post-analytics-sync' only when tweet analytics were explicitly requested."
	@exit 2

github-stars-sync:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/social-analytics social-analytics github-stars-sync

instagram-import-token:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/social-analytics social-analytics instagram-import-token

instagram-test:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/social-analytics social-analytics instagram-test

instagram-analytics-sync:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/social-analytics social-analytics instagram-sync

tiktok-auth:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/social-analytics social-analytics tiktok-auth

tiktok-test:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/social-analytics social-analytics tiktok-test

tiktok-analytics-sync:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/social-analytics social-analytics tiktok-sync

tiktok-public-audience-sync:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/social-analytics social-analytics tiktok-public-audience-sync

social-analytics-test:
	PYTHONPATH=tools/social-analytics/src python3 -m unittest discover -s tools/social-analytics/tests -v

# Experimental unified pull through Phyllo. This remains separate from the
# dashboard and routine analytics sync until its coverage proves useful.
phyllo-sync:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/phyllo-analytics phyllo-analytics sync

phyllo-tiktok-sync:
	UV_CACHE_DIR=build/uv-cache uv run --project tools/phyllo-analytics phyllo-analytics sync --platform tiktok

phyllo-test:
	PYTHONPATH=tools/phyllo-analytics/src python3 -m unittest discover -s tools/phyllo-analytics/tests -v

# Default dashboard refresh. X is follower-only by design; this target never
# requests tweet-level X metadata. TikTok content uses Phyllo while its follower
# count uses the freshest timestamped provider or public-profile observation.
# GitHub stars use the public repository API.
analytics-sync: youtube-analytics-sync x-audience-sync instagram-analytics-sync phyllo-tiktok-sync tiktok-public-audience-sync github-stars-sync

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
