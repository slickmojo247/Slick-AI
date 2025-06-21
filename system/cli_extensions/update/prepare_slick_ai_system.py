from flask import Flask, jsonify, request  # send_from_directory might not be needed if using static_folder
from ai_system import AIIntegration
import csv
import os

# Function to load configuration from slick_env_config.csv
def load_config(relative_config_path='../../slick_env_config.csv'):
    """Loads configuration from a CSV file relative to this script's location."""
    config = {}
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.normpath(os.path.join(base_dir, relative_config_path))

    default_config = {
        'FLASK_RUN_HOST': '127.0.0.1',
        'FLASK_RUN_PORT': 5000,
        'SLICK_DEBUG': True,
        'SLICK_UI_ENABLED': True,
        'SLICK_EXPLORER_ENABLED': True,
        'OPENAI_API_KEY': None,
        'DEEPSEEK_API_KEY': None
    }

    try:
        with open(config_file_path, mode='r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row and row[0].strip() and not row[0].strip().startswith('#') and len(row) == 2:
                    key, value = row[0].strip(), row[1].strip()
                    if value.lower() == 'true':
                        config[key] = True
                    elif value.lower() == 'false':
                        config[key] = False
                    elif value.isdigit(): # For port numbers and other simple integers
                        config[key] = int(value)
                    else:
                        config[key] = value # Store as string
    except FileNotFoundError:
        print(f"Warning: Configuration file '{config_file_path}' not found. Using default settings.")
        return default_config.copy()
    except Exception as e:
        print(f"Warning: Error reading configuration file '{config_file_path}': {e}. Using default settings.")
        return default_config.copy()

    # Merge defaults: CSV values override defaults, but ensure all default keys are present.
    final_config = default_config.copy()
    final_config.update(config)
    return final_config

# Load configuration
config = load_config()

# Determine the path to the static HTML files
# app.py is expected to be in ./private_ai/slick_ai/
# HTML files are in ./private_ai/galactic_html/
current_script_dir = os.path.dirname(os.path.abspath(__file__))
static_folder_path = os.path.normpath(os.path.join(current_script_dir, '../galactic_html'))

# Initialize Flask App
# static_url_path='' means files in static_folder_path are served from the root URL path
# e.g., if static_folder_path contains 'style.css', it's accessible via '/style.css'
app = Flask(__name__, static_folder=static_folder_path, static_url_path='')

# AI Integration
try:
    ai_integration = AIIntegration()
except Exception as e:
    print(f"AI Integration Error: {str(e)}")
    ai_integration = None

# Endpoint to serve the Galactic Generation Explorer HTML
@app.route('/api/explorer', methods=['GET'])
def serve_main_explorer_html():
    if config.get('SLICK_UI_ENABLED', False) or config.get('SLICK_EXPLORER_ENABLED', False):
        # Flask's send_static_file will look in the `static_folder`
        return app.send_static_file('Galactic_Generation_Explorer.html')
    return jsonify({"message": "UI not enabled in configuration."}), 404

# AI Query Endpoint
@app.route('/api/ai/query', methods=['POST'])
def ai_query():
    if not ai_integration:
        return jsonify({"error": "AI integration not available"}), 500
    
    data = request.json
    response = ai_integration.process_query(
        data.get('query'),
        data.get('model', 'hybrid')
    )
    return jsonify({"response": response})

# Main entry point to start the server
if __name__ == "__main__":
    flask_host = config.get('FLASK_RUN_HOST', '127.0.0.1')
    try:
        flask_port = int(config.get('FLASK_RUN_PORT', 5000))
    except (ValueError, TypeError):
        print(f"Warning: Invalid FLASK_RUN_PORT value '{config.get('FLASK_RUN_PORT')}'. Using default 5000.")
        flask_port = 5000
    
    flask_debug = config.get('SLICK_DEBUG', True)

    print(f"Starting Slick AI System on http://{flask_host}:{flask_port}")
    print(f"Debug mode: {flask_debug}")
    print(f"Serving static files from: {os.path.abspath(static_folder_path)}")
    if config.get('SLICK_UI_ENABLED', False) or config.get('SLICK_EXPLORER_ENABLED', False):
        print(f"Access Galactic Generation Explorer at: http://{flask_host}:{flask_port}/api/explorer")
    
    app.run(host=flask_host, port=flask_port, debug=flask_debug)
