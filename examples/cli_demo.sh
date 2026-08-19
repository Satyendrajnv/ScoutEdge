#!/usr/bin/env bash
# ScoutEdge CLI Demonstration Script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

export PYTHONPATH="$PROJECT_ROOT/src:$PYTHONPATH"

echo "============================================================"
echo "          SCOUTEDGE CLI TERMINAL UTILITY DEMO"
echo "============================================================"

echo ""
echo "[1] Running: python3 -m scoutedge.cli version"
python3 -m scoutedge.cli version

echo ""
echo "[2] Running: python3 -m scoutedge.cli eval --demo"
python3 -m scoutedge.cli eval --demo

echo ""
echo "[3] Running: python3 -m scoutedge.cli benchmark --count 100"
python3 -m scoutedge.cli benchmark --count 100

echo ""
echo "============================================================"
echo "         SCOUTEDGE CLI DEMO EXECUTION COMPLETED"
echo "============================================================"
