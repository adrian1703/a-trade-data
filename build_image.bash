#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/project.properties"

#docker build -t "$PROJECT_NAME:$VERSION" "$SCRIPT_DIR"
docker build --no-cache -t "$PROJECT_NAME:$VERSION" "$SCRIPT_DIR"
