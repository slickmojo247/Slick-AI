#!/bin/bash
BASE_DIR="/home/slyslickmojo/Slick_AI/system/cli_extensions/update"

for file in "$BASE_DIR"/*.py; do
    echo "➡️ Training on $file..."
    ./slick check-syntax --file "$file"
    ./slick train-memory --file "$file" --version v1.0 --grade green
done
