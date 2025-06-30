# Shell Assistant - Complete Project Architecture

## Project Overview

Shell Assistant is an AI-powered application that converts natural language to shell commands with comprehensive safety features, risk assessment, and contextual help. The project follows a modular architecture with clear separation of concerns.

## Core Architecture

```
shell-assist/
├── main.py                 # Application entry point & Flask server
├── ollama_interface.py     # AI/LLM integration layer
├── command_executor.py     # Command execution & safety
├── distro_detector.py      # System detection
├── user_info.py           # User context & permissions
├── cli.py                 # Enhanced CLI interface
├── templates/
│   └── index.html         # Web UI frontend
├── quickstart-*.sh        # Setup scripts
├── requirements.txt       # Dependencies
└── test_*.py             # Testing modules
```

## File-by-File Breakdown

### 1. **main.py** - Application Entry Point
**Purpose**: Central orchestrator and Flask web server

**Key Functions**:
- Initializes Flask web application
- Sets up system detection and user context
- Provides web API endpoints (`/interpret`, `/execute`)
- Handles CLI mode switching
- Manages application startup

**Integration Points**:
- Imports all core modules
- Creates global `DISTRO_INFO` and `USER_INFO` objects
- Routes web requests to appropriate handlers
- Switches between web and CLI modes

**API Endpoints**:
- `GET /` - Serves the web interface
- `POST /interpret` - Converts natural language to commands
- `POST /execute` - Executes shell commands safely

### 2. **ollama_interface.py** - AI Integration Layer
**Purpose**: Handles all AI/LLM interactions using Ollama

**Key Functions**:
- `interpret_command()` - Main AI function
- Platform-specific prompt engineering
- Structured JSON output parsing
- Risk assessment and help generation

**AI Features**:
- **Platform Awareness**: Different prompts for Linux vs macOS
- **Structured Output**: Enforces JSON schema for consistent responses
- **Context Integration**: Uses system and user info in prompts
- **Help Generation**: Creates comprehensive command documentation
- **Risk Scoring**: 0-10 scale with detailed explanations

**Data Structures**:
```python
class CommandHelp(BaseModel):
    description: str
    parameters: list[str]
    examples: list[str]
    risks: list[str]
    alternatives: list[str]
    related_commands: list[str]
    risk_score: int

class CommandOutput(BaseModel):
    command: str
    requires_sudo: bool
    notes: str
    help: CommandHelp
```

### 3. **command_executor.py** - Command Execution & Safety
**Purpose**: Safely executes shell commands with platform-specific considerations

**Key Functions**:
- `execute_command()` - Main execution function
- `is_safe_command()` - Safety validation
- `filter_unnecessary_sudo()` - Removes unnecessary sudo usage
- `get_preferred_command()` - Platform-specific command selection

**Safety Features**:
- **Command Validation**: Checks for dangerous operations
- **Permission Filtering**: Removes unnecessary sudo usage
- **Platform Optimization**: Uses GNU tools on macOS when available
- **Error Handling**: Comprehensive exception management
- **Environment Setup**: Proper user context and permissions

**Safety Checks**:
- Blocks system-critical operations
- Validates file paths and permissions
- Prevents accidental data loss
- Ensures user space operations

### 4. **distro_detector.py** - System Detection
**Purpose**: Identifies and provides system information for platform-specific behavior

**Key Functions**:
- `get_distro_info()` - Detects operating system and distribution
- Multiple fallback methods for different systems

**Platform Support**:
- **Linux**: Uses `lsb_release`, `neofetch`, `/etc/os-release`
- **macOS**: Uses `sw_vers`, `system_profiler`
- **Fallbacks**: Generic system information when specific tools unavailable

**Integration**:
- Provides context to AI prompts
- Enables platform-specific command generation
- Helps with user interface customization

### 5. **user_info.py** - User Context & Permissions
**Purpose**: Manages user information and permission context

**Key Functions**:
- `get_user_info()` - Comprehensive user information gathering
- `is_in_home_directory()` - Path safety validation

**User Data Collected**:
- Username, UID, GID
- Home directory and shell
- Platform-specific folder structure
- Operating system type

**Platform Differences**:
- **Linux**: Standard Unix user structure
- **macOS**: Handles different folder naming (Movies vs Videos)
- **Fallbacks**: Graceful handling when system calls fail

### 6. **cli.py** - Enhanced CLI Interface
**Purpose**: Provides a rich, interactive command-line interface

**Key Features**:
- **Rich Library Integration**: Colors, animations, formatting
- **Interactive Prompts**: User-friendly command input
- **Command History**: Tracks and displays command history
- **System Information**: Shows system details
- **Loading Animations**: Visual feedback during processing
- **Risk Visualization**: Color-coded risk levels

**CLI Components**:
- `EnhancedCLI` class with comprehensive UI methods
- Interactive command loop with error handling
- Rich formatting with tables, panels, and progress bars
- Command confirmation and execution flow

### 7. **templates/index.html** - Web User Interface
**Purpose**: Modern, responsive web interface for the application

**Design Features**:
- **Catppuccin Theme**: Beautiful dark/light theme support
- **Responsive Design**: Works on desktop and mobile
- **Modern UI**: Glassmorphism effects, animations
- **Real-time Updates**: Dynamic command interpretation
- **Risk Visualization**: Color-coded risk levels and warnings

**Key Components**:
- Theme toggle (dark/light mode)
- Command input with real-time interpretation
- Help section with collapsible details
- Risk score display with color coding
- Command execution with results display

### 8. **quickstart-linux.sh & quickstart-macos.sh** - Setup Scripts
**Purpose**: Automated installation and setup for different platforms

**Setup Process**:
1. **Ollama Installation**: Installs AI backend
2. **Model Download**: Pulls recommended AI model
3. **Python Environment**: Creates virtual environment
4. **Dependencies**: Installs all required packages
5. **Verification**: Checks installation success
6. **Launch Options**: Provides interface choices

**Platform Differences**:
- **Linux**: Uses curl-based Ollama installation
- **macOS**: Uses Homebrew for Ollama
- **Dependency Management**: Platform-specific package handling

### 9. **check_dependencies.py** - Dependency Management
**Purpose**: Validates that all required packages are installed

**Features**:
- **Version Checking**: Ensures compatible package versions
- **Import Validation**: Tests actual package availability
- **Exit Codes**: Provides meaningful status codes
- **Error Reporting**: Clear missing/outdated package information

### 10. **test_help.py & test_risk_scoring.py** - Testing Modules
**Purpose**: Demonstrates and validates core features

**Test Coverage**:
- **Help System**: Tests contextual help generation
- **Risk Scoring**: Validates risk assessment accuracy
- **Command Interpretation**: Tests AI command generation
- **Platform Compatibility**: Ensures cross-platform functionality

## Data Flow Architecture

### 1. **Web Interface Flow**:
```
User Input → main.py → ollama_interface.py → AI Model → 
Structured Response → command_executor.py → Results → Web UI
```

### 2. **CLI Interface Flow**:
```
User Input → cli.py → ollama_interface.py → AI Model → 
Structured Response → command_executor.py → Results → CLI Display
```

### 3. **Safety Flow**:
```
Command → is_safe_command() → Risk Assessment → 
User Confirmation → Execution → Results
```

## Key Integration Points

### 1. **AI Integration**:
- `ollama_interface.py` communicates with Ollama AI backend
- Structured JSON output ensures consistent responses
- Platform-specific prompts optimize command generation

### 2. **Safety Integration**:
- `command_executor.py` validates all commands before execution
- Risk scoring provides user awareness
- Permission checking prevents unauthorized operations

### 3. **Platform Integration**:
- `distro_detector.py` and `user_info.py` provide system context
- Platform-specific behavior in all components
- Graceful fallbacks for different system configurations

### 4. **Interface Integration**:
- Both web and CLI interfaces use the same backend
- Consistent command interpretation across interfaces
- Shared safety and validation mechanisms

## Error Handling Strategy

### 1. **Graceful Degradation**:
- Multiple fallback methods for system detection
- Alternative approaches when primary methods fail
- Clear error messages for user guidance

### 2. **Safety First**:
- Command validation before execution
- User confirmation for risky operations
- Comprehensive error reporting

### 3. **Platform Compatibility**:
- Cross-platform command generation
- System-specific optimizations
- Consistent behavior across Linux and macOS

## Security Considerations

### 1. **Command Validation**:
- Blocks dangerous system operations
- Validates file paths and permissions
- Prevents command injection attacks

### 2. **User Context**:
- Respects user permissions
- Operates within user space by default
- Clear sudo requirement warnings

### 3. **AI Safety**:
- Structured output prevents arbitrary command generation
- Risk scoring provides transparency
- User confirmation for all operations

## Performance Optimizations

### 1. **Caching**:
- System information cached at startup
- User context stored globally
- Reduced repeated system calls

### 2. **Efficient Execution**:
- Platform-specific command optimization
- Minimal subprocess overhead
- Streamlined AI prompt engineering

### 3. **Responsive UI**:
- Asynchronous command interpretation
- Real-time feedback and animations
- Optimized web interface rendering

This architecture provides a robust, scalable, and user-friendly system for AI-powered command line assistance with comprehensive safety features and cross-platform compatibility. 