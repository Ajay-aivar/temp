#!/usr/bin/env bash
# MCP Inspector UI — uses public npm registry (Syngene CodeArtifact blocks npx by default)
set -euo pipefail
cd "$(dirname "$0")"
export NPM_CONFIG_REGISTRY=https://registry.npmjs.org
exec npx --yes @modelcontextprotocol/inspector uv run server.py
