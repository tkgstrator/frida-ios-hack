#!/bin/zsh

sudo chown -R vscode:vscode node_modules
poetry install
# bun install --frozen-lockfile --ignore-scripts