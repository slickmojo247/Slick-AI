#!/bin/bash
slick check-syntax --file update/Merged_slick_stuff_1.csv
slick inspect-logic --file update/Merged_slick_stuff_1.csv --tag session-boot
slick train-memory --file update/Merged_slick_stuff_1.csv --version v1.0 --grade green
slick apply-cohesion --file update/Super_merge.csv --output sessions/cohesion_session.json
slick session-log --input sessions/cohesion_session.json --output sessions/logged_session.json
slick check-syntax --file update/Merged_slick_stuff_3.csv
slick inspect-logic --file update/Unified_AI_control.py --version v3.2 --grade yellow --tag intel-control
slick train-memory --file update/Unified_AI_control.py --version v3.2 --grade yellow
slick session-log --input sessions/logged_session.json --output sessions/final_cohesion_v3.2.json
cp -v sessions/logged_session.json archive/final_snapshot_$(date +%Y-%m).json
