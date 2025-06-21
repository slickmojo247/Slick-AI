import os
import sys
import time
import logging
from datetime import datetime
from flask import Flask, render_template_string
from flask_socketio import SocketIO
import threading
import subprocess

# Initialize Flask with compatible config
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

class DevDashboard:
    def __init__(self):
        self.logger = self.setup_logger()
        self.config = {
            "core_path": "core/",
            "components": ["main.py", "core/Slick_AI_Command_Interface.py"]
        }
        self.cli_process = None
    
    def setup_logger(self):
        logger = logging.getLogger('SlickAI')
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(ch)
        return logger
    
    def run_cli(self):
        """Run CLI in background"""
        self.cli_process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        threading.Thread(target=self.forward_output, daemon=True).start()
    
    def forward_output(self):
        """Forward CLI output to WebSocket"""
        while True:
            line = self.cli_process.stdout.readline()
            if line:
                socketio.emit('cli_output', {'data': line.strip()})
            time.sleep(0.1)

@app.route('/')
def index():
    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head><title>Slick AI</title>
            <style>body {font-family: monospace;}</style>
        </head>
        <body>
            <h1>Slick AI Dashboard</h1>
            <div id="output" style="border:1px solid #ccc; padding:10px;"></div>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.4.1/socket.io.min.js"></script>
            <script>
                const socket = io();
                socket.on('cli_output', function(data) {
                    const output = document.getElementById('output');
                    output.innerHTML += data.data + '<br>';
                    output.scrollTop = output.scrollHeight;
                });
            </script>
        </body>
        </html>
    """)

if __name__ == "__main__":
    dashboard = DevDashboard()
    dashboard.run_cli()
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, use_reloader=False)