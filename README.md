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
- Part of the Lushy.app Visual Vocabulary ecosystem

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
## License
MIT

## Author
Dal Marsters
