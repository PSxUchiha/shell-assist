import os
import sys
from flask import Flask, request, render_template, jsonify

# Import our custom modules
from distro_detector import get_distro_info
from command_executor import execute_command, is_safe_command, filter_unnecessary_sudo
from ollama_interface import interpret_command
from user_info import get_user_info

# Import enhanced CLI
try:
    from cli import EnhancedCLI
    CLI_AVAILABLE = True
except ImportError:
    CLI_AVAILABLE = False
    print("Warning: CLI mode not available. Install required packages: pip install rich colorama")

app = Flask(__name__)

# Get distribution and user info at startup
DISTRO_INFO = get_distro_info()
USER_INFO = get_user_info()

print(f"Detected system distribution:\n{DISTRO_INFO}")
print(f"User information:\n{USER_INFO}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/interpret', methods=['POST'])
def interpret():
    user_input = request.json.get('command', '')
    print(f"User input (interpret): {user_input}")
    try:
        command_output = interpret_command(user_input, DISTRO_INFO, USER_INFO)
        command = command_output.command
        notes = command_output.notes
        if command_output.requires_sudo:
            if notes:
                notes = f"This command requires sudo privileges. {notes}"
            else:
                notes = "This command requires sudo privileges."
        print(f"Interpreted command: {command}")
        print(f"Notes: {notes}")
        return jsonify({
            'interpreted_command': command,
            'notes': notes,
            'help': {
                'description': command_output.help.description,
                'parameters': command_output.help.parameters,
                'examples': command_output.help.examples,
                'risks': command_output.help.risks,
                'alternatives': command_output.help.alternatives,
                'related_commands': command_output.help.related_commands,
                'risk_score': command_output.help.risk_score
            }
        })
    except Exception as e:
        return jsonify({
            'interpreted_command': f"echo 'Error: {str(e)}'",
            'notes': f"An error occurred: {str(e)}",
            'help': {
                'description': 'Error occurred while interpreting command',
                'parameters': [],
                'examples': [],
                'risks': ['Command may not work as expected'],
                'alternatives': ['Try rephrasing your request'],
                'related_commands': [],
                'risk_score': 0
            }
        }), 400

@app.route('/execute', methods=['POST'])
def execute():
    shell_command = request.json.get('command', '')
    print(f"User input (execute): {shell_command}")
    # Check if command is safe and execute
    if not is_safe_command(shell_command):
        result = "This command requires manual intervention for safety reasons."
    else:
        result = execute_command(shell_command, USER_INFO)
    return jsonify({
        'interpreted_command': shell_command,
        'result': result
    })

def cli_mode():
    """CLI mode with colors, animations, and interactive elements"""
    if not CLI_AVAILABLE:
        print("CLI mode not available. Please install required packages:")
        print("pip install rich colorama")
        return
    
    cli = EnhancedCLI(DISTRO_INFO, USER_INFO)
    cli.run_interactive_mode(interpret_command, execute_command, is_safe_command)

if __name__ == '__main__':
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--cli':
            cli_mode()
        elif sys.argv[1] == '--help':
            print("""
Shell Assistant - AI-Powered Command Helper

Usage:
  python main.py                    # Start web interface
  python main.py --cli             # Start CLI mode (with colors and animations)
  python main.py --help            # Show this help message

CLI Mode Features:
  • Colorful interface with emojis and formatting
  • Loading animations and interactive prompts
  • Command history tracking
  • System information display
  • Better error handling and user feedback
            """)
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Use --help for available options")
    else:
        print("Starting web interface on http://127.0.0.1:5000")
        print("Use --cli for the interactive CLI mode!")
        app.run(debug=True)

