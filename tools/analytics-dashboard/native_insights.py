"""Validated, append-only native-platform evidence for the local dashboard."""

import argparse
import json
import math
import re
import shutil
import tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "youtube-series/analytics/private/native-insights"
PRECISIONS = {"exact", "rounded", "estimated"}


def image_type(path):
    with Path(path).open("rb") as stream:
        header = stream.read(12)
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png", ".png"
    if header.startswith(b"\xff\xd8\xff"):
        return "image/jpeg", ".jpg"
    if header.startswith(b"RIFF") and header[8:12] == b"WEBP":
        return "image/webp", ".webp"
    raise ValueError("Unrecognized raster screenshot data")


def numeric(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def validate(record):
    """Reject ambiguous units/provenance; retain nulls instead of inventing zeros."""
    if not isinstance(record, dict):
        raise ValueError("Snapshot must be an object")
    for key in ("metrics", "retention", "events", "screenshots"):
        if not isinstance(record.get(key, []), list) or any(not isinstance(item, dict) for item in record.get(key, [])):
            raise ValueError(f"{key} must be a list of objects")
    if not isinstance(record.get("analysis", {}), dict):
        raise ValueError("analysis must be an object")
    for key in ("id", "platform", "content_id", "title", "format", "captured_at", "period", "source_surface"):
        if not isinstance(record.get(key), str) or not record[key].strip():
            raise ValueError(f"Missing {key}")
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", record["id"]):
        raise ValueError("id must contain only letters, numbers, hyphens and underscores")
    if record["format"] not in ("short", "long"):
        raise ValueError("format must be short or long")
    if datetime.fromisoformat(record["captured_at"].replace("Z", "+00:00")).tzinfo is None:
        raise ValueError("captured_at needs a timezone")
    if not numeric(record.get("duration_seconds")) or record["duration_seconds"] == 0:
        raise ValueError("duration_seconds must be positive")
    sources = record.get("screenshots", [])
    if not sources:
        raise ValueError("At least one native screenshot is required")
    source_ids = set()
    for source in sources:
        if not isinstance(source.get("id"), str) or source["id"] in source_ids:
            raise ValueError("Screenshot IDs must be unique strings")
        source_ids.add(source["id"])
        if not isinstance(source.get("path"), str) or not source.get("label"):
            raise ValueError("Screenshot requires path and label")

    def provenance(item):
        if item.get("precision") not in PRECISIONS or item.get("source") not in source_ids:
            raise ValueError("Each measurement needs precision and a screenshot source")

    for metric in record.get("metrics", []):
        provenance(metric)
        if not metric.get("key") or not metric.get("label") or not metric.get("unit"):
            raise ValueError("Metric needs key, native label and unit")
        if metric.get("value") is not None and not numeric(metric["value"]):
            raise ValueError("Metric must be a nonnegative finite number or null")
    keys = [m["key"] for m in record.get("metrics", [])]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate metric key")
    last = -1
    for point in record.get("retention", []):
        provenance(point)
        if not numeric(point.get("seconds")) or not last < point["seconds"] <= record["duration_seconds"]:
            raise ValueError("Retention times must increase within the video duration")
        if not numeric(point.get("percent")):
            raise ValueError("Retention needs a nonnegative percentage")
        # Some platform curves can exceed 100% because of replay behavior.
        last = point["seconds"]
    record.setdefault("metrics", [])
    record.setdefault("retention", [])
    for event in record.get("events", []):
        if not numeric(event.get("seconds")) or event["seconds"] > record["duration_seconds"] or not event.get("label"):
            raise ValueError("Event needs a valid time and label")
    if record.get("events") and not record.get("media_source"):
        raise ValueError("Creative events need a final-media or transcript source")
    return record


def import_record(path, root=ROOT):
    path = Path(path).resolve()
    record = validate(json.loads(path.read_text()))
    root.mkdir(parents=True, exist_ok=True)
    destination = root / record["id"]
    if destination.exists():
        raise ValueError("Snapshot already exists; append a new capture, never overwrite")
    with tempfile.TemporaryDirectory(dir=root, prefix=".import-") as temporary:
        temporary = Path(temporary)
        for index, source in enumerate(record["screenshots"]):
            original = (path.parent / source["path"]).resolve()
            extension = original.suffix.lower()
            if extension not in (".png", ".jpg", ".jpeg", ".webp") or not original.is_file():
                raise ValueError("Screenshot must be an existing PNG, JPEG or WebP")
            _, extension = image_type(original)
            name = f"screen-{index}{extension}"
            shutil.copyfile(original, temporary / name)
            source["path"] = name
        (temporary / "record.json").write_text(json.dumps(record, indent=2) + "\n")
        temporary.rename(destination)
    return destination


def load_records(root=ROOT):
    records, errors = [], []
    for path in sorted(root.glob("*/record.json")):
        if path.parent.name.startswith("."):
            continue
        try:
            record = validate(json.loads(path.read_text()))
            if path.parent.name != record["id"]:
                raise ValueError("Snapshot directory must match id")
            for source in record["screenshots"]:
                source["url"] = f"/native-evidence/{record['id']}/{source['path']}"
            records.append(record)
        except (ValueError, TypeError, KeyError, OSError) as error:
            errors.append(f"{path.parent.name}: {error}")
    records.sort(key=lambda r: datetime.fromisoformat(r["captured_at"].replace("Z", "+00:00")), reverse=True)
    return {"records": records, "errors": errors}


def evidence_file(relative, root=ROOT):
    """Only registered raster screenshots are served, never arbitrary private files."""
    parts = relative.split("/")
    if len(parts) != 2 or any(p in ("", ".", "..") for p in parts):
        return None
    target = (root / relative).resolve()
    if root.resolve() not in target.parents or target.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
        return None
    record_path = root / parts[0] / "record.json"
    if root.resolve() not in record_path.resolve().parents:
        return None
    try:
        record = validate(json.loads(record_path.read_text()))
        if parts[1] in [s["path"] for s in record["screenshots"]] and target.is_file():
            return target
    except (ValueError, TypeError, KeyError, OSError):
        pass
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    try:
        print(import_record(args.record))
    except (ValueError, TypeError, KeyError, OSError) as error:
        parser.exit(1, f"Import failed: {error}\n")
