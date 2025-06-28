# Shell Assist

A local app that interprets natural language and safely executes shell commands on Linux and macOS. Powered by Ollama and LLMs for robust, platform-aware command generation.

## Features
- Natural language to shell command (Linux/macOS aware)
- Command confirmation before execution
- Safety checks to prevent dangerous operations
- Modern, responsive web UI
- Interactive CLI mode with colors, animations, and formatting

## Quick Start


git clone https://github.com/PSxUchiha/shell-assist.git
cd shell-assistant
# For Linux:
bash <(curl -fsSL https://raw.githubusercontent.com/PSxUchiha/shell-assist/master/scripts/quickstart-linux.sh)
# For macOS:
bash <(curl -fsSL https://raw.githubusercontent.com/PSxUchiha/shell-assist/master/scripts/quickstart-macos.sh)


The quickstart scripts will:
- Install Ollama and required dependencies
- Set up Python virtual environment
- Install all CLI dependencies (rich, colorama)
- Provide options to start web interface or CLI mode
- Offer interactive demo and help options

## Manual Setup
1. Install [Ollama](https://ollama.com/download) and run a model:
   
   # Linux
   curl -fsSL https://ollama.com/install.sh | sh
   # macOS
   brew install ollama
   ollama pull deepseek-coder
   ollama serve &
   
2. Create a Python venv and install dependencies:
   
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
3. Run the app:
   
   python main.py
   # Visit http://localhost:5000
   

## Usage Modes

### Web Interface (Default)

python main.py
# Visit http://localhost:5000


### CLI Mode (Recommended)

python main.py --cli

Features:
- 🎨 Colorful interface with emojis and formatting
- ⚡ Loading animations and interactive prompts
- 📝 Command history tracking
- 🖥️ System information display
- 🛡️ Better error handling and user feedback
- 🎯 Interactive help system

### Demo CLI

python demo_cli.py


## CLI Commands
- help - Show help information
- history - Display command history
- clear - Clear the screen
- info - Show system information
- exit or quit - Exit the application

## Requirements
- Python 3.8+
- Ollama (running locally)
- Model: deepseek-coder (recommended)
- Linux or macOS
- CLI Mode: rich and colorama packages (auto-installed via requirements.txt)

## Usage
- Enter a natural language command in the web UI or CLI.
- Review the interpreted shell command and notes.
- Confirm to execute, or cancel.
- View output and errors in the UI.

## Security
- Commands are checked for safety before execution.
- No commands are run without explicit user confirmation.

## License
MIT
