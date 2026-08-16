.PHONY: youtube-auth youtube-reauthorize youtube-analytics-sync youtube-analytics-sync-full youtube-analytics-report youtube-channel-test

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
