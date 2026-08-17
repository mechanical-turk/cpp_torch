.PHONY: youtube-auth youtube-reauthorize youtube-analytics-sync youtube-analytics-sync-full youtube-analytics-report youtube-channel-test x-auth x-test x-analytics-sync instagram-import-token instagram-test instagram-analytics-sync social-analytics-test analytics-dashboard

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
