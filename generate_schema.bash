#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCHEMA_LOC="$SCRIPT_DIR/a-trade-shared-resources"
TARGET_LOC="$SCRIPT_DIR/app/generated"

rm -r "$TARGET_LOC" &> /dev/null
mkdir -p "$TARGET_LOC"

avro-to-python "$SCHEMA_LOC" "$TARGET_LOC"
find "$TARGET_LOC" -type f -exec sed -i 's/from helpers/from app.generated.helpers/g' {} +

openapi-generator-cli generate -i "$SCRIPT_DIR/a-trade-shared-resources/a-trade-data.openapi.yaml" -g python -o "$SCRIPT_DIR/openapi" > /dev/null
openapi-generator-cli generate -i "$SCRIPT_DIR/a-trade-shared-resources/a-trade-data.openapi.yaml" -g python-flask -o "$SCRIPT_DIR/openapi" > /dev/null
cp -r "$SCRIPT_DIR/openapi/openapi_server" "$SCRIPT_DIR"