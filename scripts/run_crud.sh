#!/bin/bash

echo "=== Automated MySQL CRUD Script ==="

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Checking if mysql_server container is running..."

if ! docker ps --format '{{.Names}}' | grep -q "^mysql_server$"; then
    echo "Error: mysql_server container is not running."
    echo "Start it first with: cd docker && docker compose up -d"
    exit 1
fi

echo "mysql_server is running."

echo "Executing CRUD operations from sql/crud.sql..."

docker exec -i mysql_server mysql -u root -proot123 < "$PROJECT_ROOT/sql/crud.sql"

if [ $? -eq 0 ]; then
    echo "CRUD operations executed successfully."
else
    echo "Error while executing CRUD operations."
    exit 1
fi

echo "=== Script finished ==="