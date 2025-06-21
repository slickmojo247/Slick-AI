#!/bin/bash

# Reset network configuration
sudo unlink /etc/resolv.conf
sudo bash -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'
sudo bash -c 'echo "nameserver 1.1.1.1" >> /etc/resolv.conf'

# Test connection
echo -e "\nTesting connection to DeepSeek API..."
if curl -Is https://api.deepseek.ai | grep -q "HTTP"; then
    echo "✅ Network connection restored"
    echo "Attempting to sync pending sessions..."
    python3 ~/Slick_AI/logic/session_tools/project_syncer.py
else
    echo "❌ Still unable to connect"
    echo "Please check:"
    echo "1. Your main Windows internet connection"
    echo "2. WSL network settings"
    echo "3. Corporate VPN/firewall if applicable"
fi
