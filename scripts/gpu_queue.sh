#!/bin/bash
# Run every GPU job in order, one model at a time, inside the pinned vLLM container.
# - Logs each job to logs/gpu_budget.csv and prints the running total first.
# - Refuses to start a job if total + its estimate would pass the hard cap (270 min = 4.5 h).
# - A failed model is logged and skipped; the queue moves on.
# - Re-running the queue is safe: finished prompts are cached and skipped.
#
# Usage (on the GPU box):  nohup scripts/gpu_queue.sh configs/queue_full.txt > logs/queue.log 2>&1 &
set -u
cd "$(dirname "$0")/.."
QUEUE=${1:-configs/queue_full.txt}
CAP_MIN=${CAP_MIN:-270}
IMAGE=rocm/vllm@sha256:e0ea9a10b729573ea8598bdc073bda0ea382fe1037eec7c0761b6fa7f46baaf4
BUDGET=logs/gpu_budget.csv
mkdir -p logs results/raw
[ -f "$BUDGET" ] || echo "job_id,date,model,task,start_utc,end_utc,minutes,notes" > "$BUDGET"

used_minutes() { awk -F, 'NR>1 && $7!="" {s+=$7} END {printf "%.1f", s+0}' "$BUDGET"; }

while read -r task model est extra; do
  [[ -z "${task:-}" || "$task" == \#* ]] && continue
  if [ -f logs/STOP ]; then echo "STOP file found, ending queue"; break; fi
  used=$(used_minutes)
  echo "=== GPU minutes used so far: $used / cap $CAP_MIN. Next: $task $model (estimate $est min)"
  if awk -v u="$used" -v e="$est" -v c="$CAP_MIN" 'BEGIN{exit !(u+e>c)}'; then
    echo "Budget cap would be exceeded. Stopping before $task $model." | tee logs/STOP
    break
  fi
  start=$(date -u +%FT%TZ); t0=$(date +%s)
  job_id="$(date -u +%Y%m%d%H%M%S)_${task}"
  docker run --rm --device=/dev/kfd --device=/dev/dri --group-add video --ipc=host \
      --security-opt seccomp=unconfined --env-file /root/fairaudit/.env \
      -e HF_HUB_OFFLINE=1 -e PYTHONHASHSEED=0 \
      -v /root/hf:/root/.cache/huggingface -v "$PWD":/work -w /work "$IMAGE" \
      python3 -u -m src.$task --model "$model" $extra > "logs/${job_id}.log" 2>&1
  status=$?
  end=$(date -u +%FT%TZ); mins=$(awk -v a="$t0" -v b="$(date +%s)" 'BEGIN{printf "%.1f",(b-a)/60}')
  note="exit=$status"
  echo "$job_id,$(date -u +%F),$model,$task $extra,$start,$end,$mins,$note" >> "$BUDGET"
  echo "    finished in $mins min ($note). Log: logs/${job_id}.log"
  [ $status -ne 0 ] && tail -20 "logs/${job_id}.log"
done < "$QUEUE"
echo "=== Queue finished. Total GPU minutes: $(used_minutes)"
touch logs/QUEUE_DONE
