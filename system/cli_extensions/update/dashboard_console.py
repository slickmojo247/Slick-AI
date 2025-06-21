#!/usr/bin/env python3
import os
import subprocess
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Project root directory (adjust as needed)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.route('/')
def dashboard():
    return render_template('control_dashboard.html')

@app.route('/system-status')
def system_status():
    # Get system status from various components
    status = {
        'ai_system': check_ai_status(),
        'cli': check_cli_status(),
        'memory': check_memory_status(),
        'last_sync': get_last_sync_time()
    }
    return jsonify(status)

@app.route('/sync-code', methods=['POST'])
def sync_code():
    # Sync all code changes
    try:
        result = subprocess.run(['git', 'pull'], cwd=PROJECT_ROOT, capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({'status': 'success', 'output': result.stdout})
        else:
            return jsonify({'status': 'error', 'output': result.stderr})
    except Exception as e:
        return jsonify({'status': 'error', 'output': str(e)})

@app.route('/run-command', methods=['POST'])
def run_command():
    # Execute CLI commands
    command = request.json.get('command')
    try:
        result = subprocess.run(command.split(), cwd=PROJECT_ROOT, capture_output=True, text=True)
        return jsonify({
            'exit_code': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        })
    except Exception as e:
        return jsonify({'error': str(e)})

def check_ai_status():
    # Implement actual AI status check
    return {'status': 'active', 'components': ['core', 'cognitive', 'memory']}

def check_cli_status():
    # Implement actual CLI status check
    return {'status': 'active', 'version': '1.2.3'}

def check_memory_status():
    # Implement actual memory status check
    return {'nodes': 42, 'size': '1.2GB'}

def get_last_sync_time():
    # Implement actual sync time check
    return '2025-06-13 01:15:00'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # Add new endpoint for CLI commands
@app.route('/cli-command', methods=['POST'])
def cli_command():
    command = request.json.get('command')
    try:
        # Execute command through the same interface as terminal
        result = subprocess.run(['slick'] + command.split(), 
                               cwd=PROJECT_ROOT, 
                               capture_output=True, 
                               text=True)
        return jsonify({
            'command': command,
            'exit_code': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        })
    except Exception as e:
        return jsonify({'error': str(e)})