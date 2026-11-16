"""Run many lab.py configurations in parallel worker processes and tabulate the results.

    python sweep.py jobs.txt --workers 6 --out runs/exp1 [--device cuda]

jobs.txt: one job per line, the lab.py command-line arguments (blank lines and # comments skipped).
Each job's log goes to <out>/<n>.log and its parsed result to <out>/results.jsonl. Re-running with the
same --out skips jobs whose log already contains a RESULT line, so an interrupted sweep resumes.
"""
import argparse
import json
import shlex
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def run_job(index, line, out, device, python, script):
    log = out / f"{index:04d}.log"
    if log.exists() and "RESULT " in log.read_text():
        return index, line, log, True
    cmd = [python, str(Path(__file__).parent / script), *shlex.split(line)]
    if "--device" not in line:
        cmd += ["--device", device]
    with open(log, "w") as f:
        subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
    return index, line, log, False


def parse(log):
    for text in reversed(log.read_text().splitlines()):
        if text.startswith("RESULT "):
            return json.loads(text[7:])
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("jobs")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--out", default="runs/latest")
    p.add_argument("--device", default="cuda")
    p.add_argument("--python", default=sys.executable)
    p.add_argument("--script", default="lab.py")
    a = p.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    jobs = [l.strip() for l in Path(a.jobs).read_text().splitlines() if l.strip() and not l.startswith("#")]
    print(f"{len(jobs)} jobs, {a.workers} workers, device {a.device}", flush=True)
    start, done = time.time(), 0
    with ThreadPoolExecutor(a.workers) as pool:
        futures = [pool.submit(run_job, i, l, out, a.device, a.python, a.script) for i, l in enumerate(jobs)]
        with open(out / "results.jsonl", "a") as results:
            for fut in as_completed(futures):
                i, line, log, skipped = fut.result()
                r = parse(log)
                done += 1
                last = r["history"][-1] if r else None
                status = (f"val {last['val_acc']:.2f} test {last['test_acc']:.2f}" if last and "val_acc" in last else
                          f"test {last.get('test_acc', last.get('test')):.2f}" if last else "FAILED (see log)")
                print(f"[{done}/{len(jobs)} {time.time() - start:6.0f}s] #{i} {status}  {line}", flush=True)
                if r and not skipped:
                    results.write(json.dumps({"job": i, "line": line, "result": r}) + "\n")
                    results.flush()


if __name__ == "__main__":
    main()
