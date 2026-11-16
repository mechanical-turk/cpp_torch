#!/bin/sh
# usage: ./run_stages.sh stageM4b stageM4 ...   (runs sequentially; resumable: finished jobs are skipped)
PY=${PY:-$HOME/.venvs/content-hq-experiments/bin/python}
for s in "$@"; do
  $PY sweep.py jobs/$s.txt --workers 7 --out runs/$s --device cpu --script labsteps.py > runs/$s.log 2>&1
done
