"""
Entry point for running oscilloscope_vocabulary as a module.
Supports: python -m oscilloscope_vocabulary
"""

from oscilloscope_vocabulary.server import create_server


def main():
    """Run the MCP server."""
    server = create_server()
    server.run()


if __name__ == "__main__":
    main()
