Slick AI Project
Welcome to the Slick AI Project! This repository contains the core intelligence, interfaces, and system utilities for a versatile AI application.

Project Structure
The project is organized into logical modules:

core/: Contains the main AI logic, cognitive engine, memory management, and fundamental command processing.

logic_engine/: Houses components related to the AI's decision-making and command mapping.

config/: Stores configuration files, API management, and settings loaders.

interfaces/: Defines various interaction layers, including web, CLI, and potentially Telegram.

web/: Front-end web application files (HTML, CSS, JS, React/Vue components).

system/: Handles system-level functionalities like synchronization, version management, and command dispatching.

data/: Placeholder for datasets, knowledge bases, and other application data.

scripts/: Utility scripts, including backup tools.

backup/: (Generated) Directory for CSV backups of your project. Ignored by Git.

logs/: (Generated) Directory for log files from various processes. Ignored by Git.

Getting Started
Follow these steps to set up and run the Slick AI project on your local machine.

Prerequisites
Python 3.8+ (recommended)

pip (Python package installer)

npm (Node Package Manager) or yarn (for the web frontend)

Installation
Clone the repository:

git clone https://github.com/YourUsername/Slick_AI_Project.git
cd Slick_AI_Project

(Remember to replace YourUsername/Slick_AI_Project with your actual GitHub repository path)

Set up Python Virtual Environment:
It's highly recommended to use a virtual environment to manage project dependencies.

python3 -m venv venv
source venv/bin/activate   # On Windows, use `.\venv\Scripts\activate`

Install Python Dependencies:

pip install -r requirements.txt

Install Frontend Dependencies (if applicable):
If your web interface (interfaces/web/frontend/) is a separate React/Vue project, navigate into that directory and install its dependencies.

cd interfaces/web/frontend/
npm install  # or yarn install
cd ../../../ # Go back to the project root

Configuration
This project relies on environment variables for sensitive information like API keys.

Create a .env file:
Copy the example environment file to create your local configuration.

cp .env.example .env

Fill in your API keys:
Open the newly created .env file in a text editor and replace the placeholder values with your actual API keys from services like OpenAI, DeepSeek, Telegram, etc.

# API Keys for external services
OPENAI_API_KEY=sk-YOUR_ACTUAL_OPENAI_KEY
DEEPSEEK_API_KEY=ds-YOUR_ACTUAL_DEEPSEEK_KEY
TELEGRAM_BOT_KEY=YOUR_TELEGRAM_BOT_TOKEN

# Other non-sensitive configuration examples
LOG_LEVEL=INFO
DEBUG_MODE=True
WEB_PORT=8000

Ensure python-dotenv is installed (it's in requirements.txt) for your application to load these variables.

Running the Application
To start the main AI application:
(You'll need to identify your primary entry point, e.g., main.py or a script that starts your UnifiedController or web server)

python main.py
# OR if you have a FastAPI/Flask app:
# uvicorn interfaces.web.server:app --reload --port 8000
# OR flask run --port 8000

Refer to specific documentation or scripts within core/ or interfaces/ for precise startup commands.

To run the web frontend (if separate):

cd interfaces/web/frontend/
npm start # or yarn start

Utility Scripts
Project CSV Backup
The slick_backup.py script helps you create a comprehensive CSV backup of your project's code and metadata.

Usage:

python scripts/slick_backup.py [TARGET_DIRECTORY]

[TARGET_DIRECTORY] (Optional): Specify a custom directory to save the backup. If omitted, the backup will be saved in the backup/ directory at the project root.

Example:

python scripts/slick_backup.py
# Creates backup in ./backup/slick_backup_YYYYMMDD_HHMMSS.csv

python scripts/slick_backup.py /mnt/d/my_ai_backups
# Creates backup in /mnt/d/my_ai_backups/slick_backup_YYYYMMDD_HHMMSS.csv

Contributing
We welcome contributions! Please refer to our Contributing Guidelines (create this file if you plan to accept contributions).

License
This project is licensed under the MIT License.