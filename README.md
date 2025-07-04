# Shell Assist

A local AI-powered app that interprets natural language and safely executes shell commands on Linux and macOS. Powered by Ollama and LLMs for robust, platform-aware command generation with comprehensive contextual help and risk assessment.

## Features

### Core Features
- **Natural language to shell command** (⭐Linux/macOS aware)
- **Command confirmation** before execution
- **Safety checks** to prevent dangerous operations
- **Modern, responsive web UI** with beautiful design
- **Interactive CLI mode** with colors, animations, and formatting

### Contextual Help System
- **Detailed command descriptions** explaining what each command does
- **Parameter explanations** with purpose and usage
- **Example variations** showing different ways to use commands
- **Risk assessment** with detailed explanations of potential dangers
- **Alternative approaches** suggesting safer or more efficient methods
- **Related commands** that work well together

### Risk Scoring & Safety
- **Risk Score (0-10)** numerical assessment of command danger
- **Color-coded risk levels**:
  - **Safe (0-2)**: Read-only commands, basic information
  - **Low Risk (3-4)**: File operations in user space
  - **Medium Risk (5-6)**: System queries, network access
  - **High Risk (7-8)**: System modifications, package installs
  - **Extreme Risk (9-10)**: System-critical operations, data deletion
- **Visual warnings** with animations for dangerous commands
- **Safety-first approach** with comprehensive risk explanations

## Quick Start

```bash
git clone https://github.com/PSxUchiha/shell-assist.git
cd shell-assist
```

### For Linux:
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/PSxUchiha/shell-assist/master/quickstart-linux.sh)
```

### For macOS:
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/PSxUchiha/shell-assist/master/quickstart-macos.sh)
```

The quickstart scripts will:
- Install Ollama and required dependencies
- Set up Python virtual environment
- Install all CLI dependencies (rich, colorama)
- Provide options to start web interface or CLI mode
- Offer interactive demo and help options

## Manual Setup

1. **Install [Ollama](https://ollama.com/download)** and run a model:
   
   **Linux:**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```
   
   **macOS:**
   ```bash
   brew install ollama
   ollama pull deepseek-coder:6.7b
   ollama serve &
   ```

2. **Create a Python venv and install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   python main.py
   # Visit http://localhost:5000
   ```

## Usage Modes

### Web Interface (Default)
```bash
python main.py
# Visit http://localhost:5000
```

**Features:**
- Beautiful, responsive design with Catppuccin Mocha theme
- Real-time command interpretation
- Comprehensive help information with risk scoring
- Command confirmation dialogs
- Animated loading states and transitions
- Mobile-friendly responsive layout

### CLI Mode (Recommended)
```bash
python main.py --cli
```

**Features:**
- Colorful interface with formatting
- Loading animations and interactive prompts
- Command history tracking
- System information display
- Better error handling and user feedback
- Interactive help system
- Risk scoring with color-coded warnings

### Demo CLI
```bash
python demo_cli.py
```

## CLI Commands
- `help` - Show help information
- `history` - Display command history
- `clear` - Clear the screen
- `info` - Show system information
- `exit` or `quit` - Exit the application

## Testing Features

### Test Contextual Help
```bash
python test_help.py
```

### Test Risk Scoring
```bash
python test_risk_scoring.py
```

## Contextual Help System

### Overview
Every command generated by Shell Assist comes with comprehensive help information that includes:

- **Description**: Detailed explanation of what the command does and why it's useful
- **Parameters**: Key parameters and their purposes
- **Examples**: Example variations of the command
- **Risks**: Potential risks or side effects
- **Alternatives**: Alternative commands or approaches
- **Related Commands**: Related commands that might be useful
- **Risk Score**: Numerical assessment (0-10) with color coding

### Example Help Output

**User Input**: "show me disk usage"

**Generated Command**: `df -h`

**Risk Score**: 1/10 - Safe

**Help Information**:
- **Description**: Shows disk space usage for all mounted filesystems in human-readable format
- **Parameters**: `-h` flag displays sizes in human-readable units (KB, MB, GB)
- **Examples**: `df -h /home`, `df -h --total`
- **Risks**: None - read-only command
- **Alternatives**: `du -h` for directory-specific usage
- **Related Commands**: `du`, `lsblk`, `mount`

## Risk Scoring System

### Risk Levels

| Score | Level | Color | Description |
|-------|-------|-------|-------------|
| 0-2 | Safe | Green | Read-only commands, basic information |
| 3-4 | Low Risk | Yellow | File operations in user space |
| 5-6 | Medium Risk | Orange | System queries, network access |
| 7-8 | High Risk | Red | System modifications, package installs |
| 9-10 | Extreme Risk | Maroon | System-critical operations, data deletion |

### Risk Assessment Factors
The AI evaluates commands based on:
- **Command type**: Read-only vs destructive operations
- **Scope**: User space vs system-wide operations
- **Permissions**: Whether sudo is required
- **Data impact**: Potential for data loss
- **System impact**: Effects on system stability

### Visual Warnings
- **Color-coded risk levels** in both web and CLI interfaces
- **Animated warnings** for extreme risk commands (pulsing effect)
- **Prominent risk display** at the top of help sections
- **Detailed risk explanations** with specific dangers

## Technical Implementation

### Data Structure
```python
class CommandHelp(BaseModel):
    description: str
    parameters: list[str]
    examples: list[str]
    risks: list[str]
    alternatives: list[str]
    related_commands: list[str]
    risk_score: int  # 0-10 risk assessment

class CommandOutput(BaseModel):
    command: str
    requires_sudo: bool
    notes: str
    help: CommandHelp
```

### AI Integration
- **Enhanced Ollama interface** with structured output
- **Platform-specific prompts** for macOS and Linux
- **Comprehensive help generation** for every command
- **Risk assessment algorithm** based on command analysis
- **Safety-first approach** with detailed warnings

### Frontend Components
- **Responsive web interface** with modern design
- **Rich CLI interface** with colors and animations
- **Risk score display** with color coding
- **Help section organization** with collapsible content
- **Animation system** for visual feedback

## Benefits

### For Beginners
- **Learning Tool**: Understand what commands do before running them
- **Safety**: Know about risks and side effects with clear visual indicators
- **Exploration**: Discover related commands and alternatives
- **Confidence**: Risk scoring helps build confidence in command usage

### For Experienced Users
- **Efficiency**: Quick reference for parameter meanings
- **Discovery**: Learn about new tools and approaches
- **Best Practices**: Understand safer alternatives
- **Risk Assessment**: Make informed decisions about command execution

### For System Administrators
- **Documentation**: Built-in command documentation
- **Training**: Help train team members on proper command usage
- **Audit Trail**: Understand what commands do for compliance
- **Safety Protocols**: Risk scoring helps enforce safety policies

## Requirements
- Python 3.8+
- Ollama (running locally)
- Model: deepseek-coder:6.7b (recommended)
- Linux or macOS
- CLI Mode: rich and colorama packages (auto-installed via requirements.txt)

## Future Enhancements

### Planned Features
1. **Interactive Help**: Click on parameters to see detailed explanations
2. **Command History Help**: Learn from previously executed commands
3. **Custom Help**: User-defined help for custom commands
4. **Help Search**: Search through help content
5. **Help Export**: Export help information for documentation
6. **Risk Thresholds**: User-configurable risk level warnings
7. **Command Blocking**: Automatic blocking of extreme risk commands

### Integration Opportunities
1. **IDE Integration**: Help information in VS Code extension
2. **Mobile App**: Help content in mobile companion app
3. **API Access**: Programmatic access to help information
4. **Community Help**: User-contributed help content
5. **Risk Analytics**: Track and analyze command risk patterns

## Security
- Commands are checked for safety before execution
- No commands are run without explicit user confirmation
- Risk scoring provides clear warnings about dangerous operations
- Platform-specific safety checks for Linux and macOS
- Comprehensive risk assessment for all generated commands

## Contributing

To contribute to Shell Assist:

1. **Enhance Help Generation**: Improve the AI prompts for better help content
2. **Add Help Templates**: Create templates for common command types
3. **Improve UI**: Enhance the visual presentation of help information
4. **Add Examples**: Contribute more example commands and help content
5. **Refine Risk Scoring**: Improve the risk assessment algorithm
6. **Add Risk Templates**: Create risk assessment templates for different command types

## Testing

Run the test scripts to see the features in action:

```bash
# Test contextual help
python test_help.py

# Test risk scoring
python test_risk_scoring.py
```

These will demonstrate the help feature and risk scoring with various example commands.

## License
MIT

## Conclusion

Shell Assist transforms from a simple command interpreter into a comprehensive learning and safety tool. The contextual help system provides detailed explanations for every command, while the risk scoring system ensures users understand the potential dangers before execution. This makes shell commands more accessible, educational, and safe for users of all experience levels.
