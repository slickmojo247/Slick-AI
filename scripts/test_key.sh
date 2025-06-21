#!/bin/bash

# Read key securely
read -sp "Enter DeepSeek API key: " API_KEY
echo -e "\nTesting..."

# Test authentication
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -X POST https://api.deepseek.ai/v1/validate)

# Interpret result
case $RESPONSE in
  200) echo "✅ Key is valid and working";;
  401) echo "❌ Invalid key (unauthorized)";;
  000) echo "🛑 Network error - cannot reach API";;
  *)   echo "⚠️ Unexpected response: HTTP $RESPONSE";;
esac

# Securely unset key
unset API_KEY
