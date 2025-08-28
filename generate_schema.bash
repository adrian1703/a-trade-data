#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCHEMA_LOC="$SCRIPT_DIR/../a-trade-shared-resources"
TARGET_LOC="$SCRIPT_DIR/app/generated"

rm -r "$TARGET_LOC" &> /dev/null
mkdir -p "$TARGET_LOC"

avro-to-python "$SCHEMA_LOC" "$TARGET_LOC"
find "$TARGET_LOC" -type f -exec sed -i 's/from helpers/from app.generated.helpers/g' {} +