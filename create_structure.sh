#!/bin/bash
# Standard MCP Server Setup Pattern - Structure Generation
# Creates all directories and small configuration files automatically

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="oscilloscope-vocabulary"
PACKAGE_NAME="oscilloscope_vocabulary"

echo "🔨 Creating Standard MCP Server Structure..."
echo "Project Root: $PROJECT_ROOT"
echo "Package Name: $PACKAGE_NAME"
echo ""

# Create directory structure
echo "📁 Creating directories..."
mkdir -p "$PROJECT_ROOT/src/$PACKAGE_NAME"
mkdir -p "$PROJECT_ROOT/src/$PACKAGE_NAME/ologs"
mkdir -p "$PROJECT_ROOT/tests"
mkdir -p "$PROJECT_ROOT/docs"

echo "✅ Directories created"
echo ""

# Create __init__.py files
echo "📝 Creating package initialization files..."
touch "$PROJECT_ROOT/src/$PACKAGE_NAME/__init__.py"
cat > "$PROJECT_ROOT/src/$PACKAGE_NAME/__init__.py" << 'EOF'
"""Oscilloscope Vocabulary MCP Server - Visual vocabulary for harmonic-guided image generation."""

__version__ = "0.1.0"
__author__ = "Dal"

from .server import create_server

__all__ = ["create_server"]
EOF

touch "$PROJECT_ROOT/tests/__init__.py"
echo ""

# Create pyproject.toml
echo "📦 Creating pyproject.toml..."
cat > "$PROJECT_ROOT/pyproject.toml" << 'EOF'
[project]
name = "oscilloscope-vocabulary"
version = "0.1.0"
description = "Oscilloscope pattern visual vocabulary for harmonic-guided image generation"
readme = "README.md"
requires-python = ">=3.8"
authors = [{name = "Dal"}]
dependencies = [
    "fastmcp>=0.1.0",
    "pillow>=10.0.0",
    "numpy>=1.24.0",
    "scipy>=1.10.0",
    "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/oscilloscope_vocabulary"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
addopts = "-v --tb=short"
EOF

echo "✅ pyproject.toml created"
echo ""

# Create README.md
echo "📄 Creating README.md..."
cat > "$PROJECT_ROOT/README.md" << 'EOF'
# Oscilloscope Vocabulary MCP Server

A FastMCP server that translates between visual color language and oscilloscope frequency patterns, enabling bidirectional image transformation and guided generation.

## Features

- **Three-layer architecture**: Deterministic extraction + synthesis
- **60-70% cost savings**: Deterministic layers eliminate LLM calls
- **Visual vocabulary**: Colors encode frequency, patterns show structure
- **Bidirectional workflows**: Transform images or guide generation
- **Constraint controls**: 5 levels from strict to experimental

## Quick Start

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
./tests/run_tests.sh

# Start server
python -m oscilloscope_vocabulary.server
```

## Documentation

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design and workflows
- [EXAMPLES.md](docs/EXAMPLES.md) - Real-world examples
- [INTEGRATION.md](docs/INTEGRATION.md) - Lushy integration guide

## Project Structure

```
oscilloscope-vocabulary/
├── src/oscilloscope_vocabulary/
│   ├── server.py              # Main MCP server
│   ├── layers.py              # Layer implementations
│   └── ologs/                 # YAML olog specifications
├── tests/
│   ├── test_server.py
│   ├── test_layers.py
│   └── run_tests.sh
├── docs/
├── pyproject.toml
└── create_structure.sh / verify_structure.sh
```
EOF

echo "✅ README.md created"
echo ""

# Create tests/run_tests.sh
echo "🧪 Creating test runner..."
mkdir -p "$PROJECT_ROOT/tests"
cat > "$PROJECT_ROOT/tests/run_tests.sh" << 'EOF'
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
EOF

chmod +x "$PROJECT_ROOT/tests/run_tests.sh"
echo "✅ tests/run_tests.sh created"
echo ""

# Create placeholder olog file
echo "📋 Creating olog structure..."
cat > "$PROJECT_ROOT/src/$PACKAGE_NAME/ologs/README.md" << 'EOF'
# Olog Specifications

YAML-based specifications for oscilloscope vocabulary taxonomy:

- harmonic_profiles.yaml - Frequency distribution profiles
- constraint_levels.yaml - Constraint parameters
- color_mapping.yaml - Color-to-frequency mappings

Each olog file contains deterministic mappings for Layer 1 extraction.
EOF

echo "✅ olog structure created"
echo ""

# Create .gitignore
echo "📝 Creating .gitignore..."
cat > "$PROJECT_ROOT/.gitignore" << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Testing
.pytest_cache/
.coverage
htmlcov/

# Project
.mypy_cache/
.dmypy.json
dmypy.json
EOF

echo "✅ .gitignore created"
echo ""

# Summary
echo "════════════════════════════════════════════════════════════"
echo "✅ Standard MCP Server Structure Created Successfully!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📁 Directory structure:"
tree -L 3 -I '__pycache__|*.pyc' "$PROJECT_ROOT" 2>/dev/null || find "$PROJECT_ROOT" -type d ! -path '*/.*' | head -20
echo ""
echo "📝 Next steps:"
echo "  1. Review structure: ./verify_structure.sh"
echo "  2. Copy server.py: src/oscilloscope_vocabulary/server.py"
echo "  3. Copy tests: tests/test_*.py"
echo "  4. Install: pip install -e '.[dev]'"
echo "  5. Test: ./tests/run_tests.sh"
echo ""
