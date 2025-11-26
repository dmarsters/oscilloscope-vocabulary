#!/bin/bash
# Standard MCP Server Setup Pattern - Structure Verification
# Validates directory structure and file presence before/after pip install

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="oscilloscope-vocabulary"
PACKAGE_NAME="oscilloscope_vocabulary"

REQUIRED_DIRS=(
    "src"
    "src/$PACKAGE_NAME"
    "src/$PACKAGE_NAME/ologs"
    "tests"
    "docs"
)

REQUIRED_FILES=(
    "pyproject.toml"
    "README.md"
    "create_structure.sh"
    "verify_structure.sh"
    "src/$PACKAGE_NAME/__init__.py"
    "tests/__init__.py"
    "tests/run_tests.sh"
)

MANUAL_FILES=(
    "src/$PACKAGE_NAME/server.py"
    "src/$PACKAGE_NAME/layers.py"
    "tests/test_server.py"
    "tests/test_layers.py"
)

echo "════════════════════════════════════════════════════════════"
echo "🔍 Verifying Standard MCP Server Structure"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Project Root: $PROJECT_ROOT"
echo "Package Name: $PACKAGE_NAME"
echo ""

# Check directories
echo "📁 Checking required directories..."
MISSING_DIRS=0
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$PROJECT_ROOT/$dir" ]; then
        echo "  ✅ $dir"
    else
        echo "  ❌ $dir (MISSING)"
        MISSING_DIRS=$((MISSING_DIRS + 1))
    fi
done
echo ""

# Check auto-generated files
echo "📄 Checking auto-generated files..."
MISSING_FILES=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$PROJECT_ROOT/$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (MISSING)"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
done
echo ""

# Check manual files (not required initially)
echo "📝 Checking manual files (to be added)..."
MISSING_MANUAL=0
for file in "${MANUAL_FILES[@]}"; do
    if [ -f "$PROJECT_ROOT/$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ⏳ $file (needs to be created)"
        MISSING_MANUAL=$((MISSING_MANUAL + 1))
    fi
done
echo ""

# Summary
echo "════════════════════════════════════════════════════════════"
if [ $MISSING_DIRS -eq 0 ] && [ $MISSING_FILES -eq 0 ]; then
    echo "✅ STRUCTURE VERIFIED - Ready for manual file additions"
    echo ""
    if [ $MISSING_MANUAL -gt 0 ]; then
        echo "📝 Still need to create:"
        for file in "${MANUAL_FILES[@]}"; do
            if [ ! -f "$PROJECT_ROOT/$file" ]; then
                echo "  • $file"
            fi
        done
        echo ""
    fi
    echo "Next steps:"
    echo "  1. Create manual files listed above"
    echo "  2. Run: pip install -e '.[dev]' (from project root)"
    echo "  3. Run: ./tests/run_tests.sh"
    echo ""
    exit 0
else
    echo "❌ STRUCTURE INCOMPLETE"
    echo "Missing directories: $MISSING_DIRS"
    echo "Missing files: $MISSING_FILES"
    echo ""
    echo "Run: ./create_structure.sh"
    echo ""
    exit 1
fi
