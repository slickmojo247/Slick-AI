#!/bin/bash
git add .
echo "Commit message:"
read msg
git commit -m "$msg"
git push
