#!/bin/bash
# Chain: wait for any running queue -> pilot -> full queue. Safe to re-run (cache).
cd "$(dirname "$0")/.."
while pgrep -f "gpu_queue.sh configs/queue_smoke" >/dev/null; do sleep 20; done
scripts/gpu_queue.sh configs/queue_pilot.txt
scripts/gpu_queue.sh configs/queue_full.txt
