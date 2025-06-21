#!/bin/bash
export OPENAI_KEY="your-key-here"
export DEEPSEEK_KEY="your-key-here"
export API_KEY="slick-secret-key"

uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
