import ollama
from pydantic import BaseModel, Field
import json
import platform
import re

class CommandHelp(BaseModel):
    """Schema for detailed command help information"""
    description: str = Field(description="Detailed description of what the command does")
    parameters: list[str] = Field(default=[], description="List of key parameters and their purposes")
    examples: list[str] = Field(default=[], description="Example variations of the command")
    risks: list[str] = Field(default=[], description="Potential risks or side effects")
    alternatives: list[str] = Field(default=[], description="Alternative commands or approaches")
    related_commands: list[str] = Field(default=[], description="Related commands that might be useful")
    risk_score: int = Field(default=0, description="Risk score from 0-10, where 0 is safe and 10 is extremely dangerous")

class CommandOutput(BaseModel):
    """Schema for structured command output"""
    command: str = Field(description="The exact shell command to execute without any conversational text")
    requires_sudo: bool = Field(default=False, description="Whether this command requires sudo privileges")
    notes: str = Field(default="", description="Optional notes about the command execution")
    help: CommandHelp = Field(default_factory=lambda: CommandHelp(), description="Detailed help information for the command")

def interpret_command(user_input, distro_info, user_info):
    """
    Interpret natural language input and convert it to a shell command
    using structured output to ensure clean command responses.
    """
    system = platform.system()
    
    # Create platform-specific system prompt
    if system == "Darwin":  # macOS
        system_prompt = f"""You are a macOS command generator that converts natural language to precise shell commands.

System information:
{distro_info}

User information:
Username: {user_info['username']}
Home Directory: {user_info['home']}
Available user folders: {', '.join(user_info['folders'].keys())}

CRITICAL RULES FOR macOS COMMANDS:
1. ALWAYS prefer standard Unix/GNU utilities first:
   - File operations: ls, find, grep, cat, head, tail, less, more
   - Text processing: sed, awk, sort, uniq, wc, cut, tr
   - Compression: tar, gzip, bzip2, zip, unzip
   - Downloads: curl, wget
   - Text editing: vim, nano
   - System info: df, du, ps, top, who, date

2. ONLY use macOS-specific tools when absolutely necessary:
   - 'open' ONLY for: opening applications, launching URLs in browser, opening files with default apps
   - 'defaults' ONLY for: system preferences that can't be changed otherwise
   - 'brew' ONLY for: package installation/management
   - 'say', 'afplay', 'screencapture' ONLY when specifically requested

3. EXAMPLES of correct command choices:
   - "search for text": use 'grep -r "text" .' NOT 'open'
   - "compress folder": use 'tar -czf archive.tar.gz folder/' NOT 'open'
   - "download file": use 'curl -O url' NOT 'open'
   - "edit file": use 'vim file.txt' or 'nano file.txt' NOT 'open'
   - "check disk space": use 'df -h' NOT 'open'
   - "open website": use 'open https://example.com' (this is correct use of open)

4. NEVER use sudo unless absolutely necessary for system modifications.

5. ALWAYS provide detailed help information including:
   - Clear description of what the command does
   - Key parameters and their purposes
   - Example variations
   - Potential risks
   - Alternative approaches
   - Related commands
   - Risk score (0-10) where:
     * 0-2: Safe commands (read-only, basic info)
     * 3-4: Low risk (file operations in user space)
     * 5-6: Medium risk (system queries, network access)
     * 7-8: High risk (system modifications, package installs)
     * 9-10: Extreme risk (system-critical operations, data deletion)

Respond ONLY with a valid JSON object matching this exact schema:
{{
  "command": "the exact shell command to execute",
  "requires_sudo": false,
  "notes": "brief explanation of what the command does",
  "help": {{
    "description": "detailed description of what the command does and why it's useful",
    "parameters": ["list of key parameters and their purposes"],
    "examples": ["example variations of the command"],
    "risks": ["potential risks or side effects"],
    "alternatives": ["alternative commands or approaches"],
    "related_commands": ["related commands that might be useful"],
    "risk_score": 0
  }}
}}

NO markdown, NO explanations, NO code blocks - ONLY the JSON object."""

    else:  # Linux
        system_prompt = f"""You are a Linux command generator that converts natural language to precise shell commands.

System information:
{distro_info}

User information:
Username: {user_info['username']}
Home Directory: {user_info['home']}
Available user folders: {', '.join(user_info['folders'].keys())}

IMPORTANT RULES FOR LINUX:
1. DO NOT use sudo for operations that don't require root privileges
2. Only mark requires_sudo as true when absolutely necessary (system modifications, package installs, etc.)
3. Use appropriate Linux commands and tools
4. Prefer user-space operations over system operations
5. ALWAYS provide detailed help information including:
   - Clear description of what the command does
   - Key parameters and their purposes
   - Example variations
   - Potential risks
   - Alternative approaches
   - Related commands
   - Risk score (0-10) where:
     * 0-2: Safe commands (read-only, basic info)
     * 3-4: Low risk (file operations in user space)
     * 5-6: Medium risk (system queries, network access)
     * 7-8: High risk (system modifications, package installs)
     * 9-10: Extreme risk (system-critical operations, data deletion)

Respond ONLY with a valid JSON object matching this exact schema:
{{
  "command": "the exact shell command to execute",
  "requires_sudo": false,
  "notes": "optional explanation",
  "help": {{
    "description": "detailed description of what the command does and why it's useful",
    "parameters": ["list of key parameters and their purposes"],
    "examples": ["example variations of the command"],
    "risks": ["potential risks or side effects"],
    "alternatives": ["alternative commands or approaches"],
    "related_commands": ["related commands that might be useful"],
    "risk_score": 0
  }}
}}

NO markdown, NO explanations, NO code blocks - ONLY the JSON object."""

    try:
        # Get the schema for structured output
        schema = CommandOutput.model_json_schema()
        
        # Call Ollama with structured output
        response = ollama.chat(
            model='deepseek-coder:6.7b',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_input}
            ],
            format=schema
        )
        
        # Handle different response formats (compatibility fix)
        content = None
        
        # Try new API format first (ollama >= 0.4.0)
        if hasattr(response, 'message') and hasattr(response.message, 'content'):
            content = response.message.content
        # Try alternative new API format
        elif hasattr(response, 'message') and isinstance(response.message, dict):
            content = response.message.get('content')
        # Try old API format (ollama <= 0.1.x) - Dictionary response
        elif isinstance(response, dict):
            if 'message' in response and isinstance(response['message'], dict):
                content = response['message'].get('content')
            elif 'message' in response and isinstance(response['message'], str):
                content = response['message']
            elif 'content' in response:
                content = response['content']
            elif 'response' in response:  # Some versions use 'response' key
                content = response['response']
            else:
                # Last resort - try to extract any text content
                content = str(response)
        else:
            # Fallback for unknown formats
            content = str(response)

        # Parse the JSON content
        if isinstance(content, str):
            try:
                parsed_content = json.loads(content)
            except json.JSONDecodeError:
                # If content is not valid JSON, try to extract it
                # Sometimes the model wraps JSON in markdown code blocks
                json_match = re.search(r'``````', content, re.DOTALL)
                if json_match:
                    parsed_content = json.loads(json_match.group(1))
                else:
                    # Try to find any JSON-like structure
                    json_match = re.search(r'(\{.*?\})', content, re.DOTALL)
                    if json_match:
                        parsed_content = json.loads(json_match.group(1))
                    else:
                        # If no JSON found, create a fallback response
                        parsed_content = {
                            "command": f"echo 'Unable to parse command from: {content[:100]}...'",
                            "requires_sudo": False,
                            "notes": "Failed to parse model response as JSON",
                            "help": {
                                "description": "This is a fallback command due to parsing issues",
                                "parameters": [],
                                "examples": [],
                                "risks": ["Command may not work as expected"],
                                "alternatives": ["Try rephrasing your request"],
                                "related_commands": [],
                                "risk_score": 0
                            }
                        }
        else:
            parsed_content = content

        # Validate with Pydantic
        command_output = CommandOutput(**parsed_content)
        
        return command_output
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Model returned invalid JSON: {e}")
    except Exception as e:
        raise ValueError(f"Model did not return valid output: {e}")
