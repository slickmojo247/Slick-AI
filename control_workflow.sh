#!/bin/bash
BASE_DIR="/home/slyslickmojo/Slick_AI/system/cli_extensions"

# Step 1
./slick check-syntax --file $BASE_DIR/update/Merged_slick_stuff_1.csv

# Step 2
./slick inspect-logic --file $BASE_DIR/update/Merged_slick_stuff_1.csv --tag session-boot

# Step 3
./slick train-memory --file $BASE_DIR/update/Merged_slick_stuff_1.csv --version v1.0 --grade green

# Step 4
./slick apply-cohesion --file $BASE_DIR/update/Super_merge.csv --output $BASE_DIR/sessions/cohesion_session.json

# Step 5
./slick session-log --input $BASE_DIR/sessions/cohesion_session.json --output $BASE_DIR/sessions/logged_session.json

# Step 6
./slick check-syntax --file $BASE_DIR/update/Merged_slick_stuff_3.csv

# Step 7 - fixed (removed invalid args)
./slick inspect-logic --file $BASE_DIR/update/Unified_AI_control.py --tag intel-control

# Step 8
./slick train-memory --file $BASE_DIR/update/Unified_AI_control.py --version v3.2 --grade yellow

# Step 9
./slick session-log --input $BASE_DIR/sessions/logged_session.json --output $BASE_DIR/sessions/final_cohesion_v3.2.json

# Step 10 - fixed (copy correct final file)
cp -v $BASE_DIR/sessions/final_cohesion_v3.2.json $BASE_DIR/archive/final_snapshot_$(date +\%Y-\%m).json
