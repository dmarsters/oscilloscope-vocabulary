#!/bin/bash
# Test runner for oscilloscope-vocabulary MCP server

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "🧪 Running tests from: $PROJECT_ROOT"
echo ""

cd "$PROJECT_ROOT"

# Run pytest with coverage
python -m pytest tests/ -v --tb=short "$@"

echo ""
echo "✅ All tests passed!"
