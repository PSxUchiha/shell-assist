import os
import sys
import time
import threading
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.align import Align
from rich import box
from colorama import init, Fore, Back, Style
import platform

# Initialize colorama for cross-platform color support
init(autoreset=True)

class EnhancedCLI:
    def __init__(self, distro_info, user_info):
        self.console = Console()
        self.distro_info = distro_info
        self.user_info = user_info
        self.command_history = []
        
    def print_banner(self):
        """Display a colorful banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🚀 SHELL ASSISTANT 🚀                     ║
║                 Your AI-Powered Command Helper               ║
╚══════════════════════════════════════════════════════════════╝
        """
        self.console.print(Panel(banner, style="bold blue", box=box.DOUBLE))
    
    def print_system_info(self):
        """Display system information in a formatted table"""
        table = Table(title="🖥️  System Information", show_header=True, header_style="bold magenta")
        table.add_column("Property", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")
        
        # Add system info
        system = platform.system()
        table.add_row("Operating System", f"{system} {platform.release()}")
        table.add_row("Architecture", platform.machine())
        table.add_row("Python Version", platform.python_version())
        
        # Add user info
        table.add_row("Username", self.user_info.get('username', 'Unknown'))
        table.add_row("Home Directory", self.user_info.get('home', 'Unknown'))
        
        # Add distro info if available
        if self.distro_info:
            if isinstance(self.distro_info, str):
                lines = self.distro_info.split('\n')
                for line in lines[:3]:  # Show first 3 lines
                    if line.strip():
                        table.add_row("Distribution", line.strip())
                        break
            else:
                table.add_row("Distribution", str(self.distro_info))
        
        self.console.print(table)
    
    def loading_animation(self, message: str, duration: float = 2.0):
        """Show a loading animation with dots"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            task = progress.add_task(message, total=None)
            time.sleep(duration)
    
    def typing_animation(self, text: str, speed: float = 0.03):
        """Simulate typing animation"""
        for char in text:
            self.console.print(char, end="", style="green")
            time.sleep(speed)
        self.console.print()
    
    def print_command_prompt(self):
        """Display an interactive command prompt"""
        prompt_text = Text()
        prompt_text.append("🤖 ", style="bold blue")
        prompt_text.append("What would you like me to help you with? ", style="bold white")
        prompt_text.append("(type 'help' for commands, 'exit' to quit)", style="dim")
        
        return Prompt.ask(prompt_text)
    
    def print_help(self):
        """Display help information"""
        help_text = """
🎯 Available Commands:
• help - Show this help message
• history - Show command history
• clear - Clear the screen
• exit/quit - Exit the application
• info - Show system information

💡 Tips:
• Use natural language to describe what you want to do
• Examples: "show me disk usage", "find all Python files", "check system status"
• The AI will interpret your request and suggest appropriate commands
        """
        self.console.print(Panel(help_text, title="📚 Help", style="bold yellow"))
    
    def print_command_history(self):
        """Display command history"""
        if not self.command_history:
            self.console.print("📝 No commands in history yet.", style="dim")
            return
        
        table = Table(title="📝 Command History", show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", no_wrap=True)
        table.add_column("Command", style="green")
        table.add_column("Status", style="yellow")
        
        for i, (cmd, status) in enumerate(self.command_history[-10:], 1):  # Show last 10
            status_icon = "✅" if status == "success" else "❌" if status == "error" else "⚠️"
            table.add_row(str(i), cmd[:50] + "..." if len(cmd) > 50 else cmd, status_icon)
        
        self.console.print(table)
    
    def get_risk_level(self, risk_score: int) -> tuple[str, str]:
        """Get risk level description and color based on risk score"""
        if risk_score <= 2:
            return "🟢 Safe", "green"
        elif risk_score <= 4:
            return "🟡 Low Risk", "yellow"
        elif risk_score <= 6:
            return "🟠 Medium Risk", "orange3"
        elif risk_score <= 8:
            return "🔴 High Risk", "red"
        else:
            return "⛔ Extreme Risk", "bold red"

    def print_interpreted_command(self, command: str, notes: str = "", requires_sudo: bool = False, help_info: dict = None):
        """Display the interpreted command with formatting and detailed help"""
        # Create a panel for the command
        command_text = Text()
        command_text.append("🔧 ", style="bold blue")
        command_text.append("Interpreted Command:", style="bold white")
        
        command_panel = Panel(
            f"\n{command}\n",
            title=command_text,
            style="bold green" if not requires_sudo else "bold red",
            border_style="green" if not requires_sudo else "red"
        )
        
        self.console.print(command_panel)
        
        # Show risk score if available
        if help_info and 'risk_score' in help_info:
            risk_level, risk_color = self.get_risk_level(help_info['risk_score'])
            risk_text = Text()
            risk_text.append("⚠️ ", style="bold red")
            risk_text.append("Risk Level: ", style="bold white")
            risk_text.append(f"{risk_level} ({help_info['risk_score']}/10)", style=risk_color)
            risk_panel = Panel(risk_text, style=risk_color, border_style=risk_color)
            self.console.print(risk_panel)
        
        # Show notes if any
        if notes:
            notes_text = Text()
            notes_text.append("📝 ", style="bold yellow")
            notes_text.append("Notes:", style="bold white")
            notes_panel = Panel(notes, title=notes_text, style="bold yellow")
            self.console.print(notes_panel)
        
        # Show sudo warning if needed
        if requires_sudo:
            sudo_warning = Text()
            sudo_warning.append("⚠️ ", style="bold red")
            sudo_warning.append("This command requires sudo privileges!", style="bold red")
            self.console.print(Panel(sudo_warning, style="bold red", border_style="red"))
        
        # Show detailed help information if available
        if help_info:
            self.print_detailed_help(help_info)
    
    def print_detailed_help(self, help_info: dict):
        """Display detailed help information in an organized format"""
        # Description
        if help_info.get('description'):
            desc_text = Text()
            desc_text.append("📖 ", style="bold blue")
            desc_text.append("Description:", style="bold white")
            desc_panel = Panel(help_info['description'], title=desc_text, style="bold blue")
            self.console.print(desc_panel)
        
        # Parameters
        if help_info.get('parameters') and len(help_info['parameters']) > 0:
            params_text = Text()
            params_text.append("⚙️ ", style="bold cyan")
            params_text.append("Parameters:", style="bold white")
            
            params_content = "\n".join([f"• {param}" for param in help_info['parameters']])
            params_panel = Panel(params_content, title=params_text, style="bold cyan")
            self.console.print(params_panel)
        
        # Examples
        if help_info.get('examples') and len(help_info['examples']) > 0:
            examples_text = Text()
            examples_text.append("💡 ", style="bold green")
            examples_text.append("Examples:", style="bold white")
            
            examples_content = "\n".join([f"• {example}" for example in help_info['examples']])
            examples_panel = Panel(examples_content, title=examples_text, style="bold green")
            self.console.print(examples_panel)
        
        # Risks
        if help_info.get('risks') and len(help_info['risks']) > 0:
            risks_text = Text()
            risks_text.append("⚠️ ", style="bold red")
            risks_text.append("Risks:", style="bold white")
            
            risks_content = "\n".join([f"• {risk}" for risk in help_info['risks']])
            risks_panel = Panel(risks_content, title=risks_text, style="bold red")
            self.console.print(risks_panel)
        
        # Alternatives
        if help_info.get('alternatives') and len(help_info['alternatives']) > 0:
            alt_text = Text()
            alt_text.append("🔄 ", style="bold magenta")
            alt_text.append("Alternatives:", style="bold white")
            
            alt_content = "\n".join([f"• {alt}" for alt in help_info['alternatives']])
            alt_panel = Panel(alt_content, title=alt_text, style="bold magenta")
            self.console.print(alt_panel)
        
        # Related Commands
        if help_info.get('related_commands') and len(help_info['related_commands']) > 0:
            related_text = Text()
            related_text.append("🔗 ", style="bold yellow")
            related_text.append("Related Commands:", style="bold white")
            
            related_content = "\n".join([f"• {cmd}" for cmd in help_info['related_commands']])
            related_panel = Panel(related_content, title=related_text, style="bold yellow")
            self.console.print(related_panel)
    
    def print_execution_result(self, result, command: str):
        """Display command execution results with formatting"""
        if isinstance(result, dict):
            # Structured result
            result_panel = Panel(
                f"[bold green]Command executed successfully![/bold green]\n\n"
                f"[bold]Output:[/bold]\n{result.get('stdout', 'No output')}\n\n"
                f"[bold]Return Code:[/bold] {result.get('returncode', 'Unknown')}",
                title="✅ Execution Result",
                style="bold green"
            )
            self.console.print(result_panel)
            
            if result.get('stderr'):
                error_panel = Panel(
                    result['stderr'],
                    title="⚠️ Errors/Warnings",
                    style="bold yellow"
                )
                self.console.print(error_panel)
        else:
            # Simple result
            result_panel = Panel(
                str(result),
                title="✅ Execution Result",
                style="bold green"
            )
            self.console.print(result_panel)
    
    def print_error(self, error_message: str):
        """Display error messages with formatting"""
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error:", style="bold red")
        error_panel = Panel(error_message, title=error_text, style="bold red")
        self.console.print(error_panel)
    
    def print_success(self, message: str):
        """Display success messages with formatting"""
        success_text = Text()
        success_text.append("✅ ", style="bold green")
        success_text.append("Success:", style="bold green")
        success_panel = Panel(message, title=success_text, style="bold green")
        self.console.print(success_panel)
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_banner()
    
    def run_interactive_mode(self, interpret_command_func, execute_command_func, is_safe_command_func):
        """Run the enhanced interactive CLI mode"""
        self.clear_screen()
        self.print_system_info()
        self.console.print()
        
        while True:
            try:
                # Get user input
                user_input = self.print_command_prompt()
                
                # Handle special commands
                if user_input.lower() in ['exit', 'quit']:
                    self.console.print("👋 Goodbye! Thanks for using Shell Assistant!", style="bold blue")
                    break
                elif user_input.lower() == 'help':
                    self.print_help()
                    continue
                elif user_input.lower() == 'history':
                    self.print_command_history()
                    continue
                elif user_input.lower() == 'clear':
                    self.clear_screen()
                    self.print_system_info()
                    self.console.print()
                    continue
                elif user_input.lower() == 'info':
                    self.print_system_info()
                    continue
                elif not user_input.strip():
                    continue
                
                # Show loading animation while interpreting
                with self.console.status("[bold blue]🤖 Interpreting your request...", spinner="dots"):
                    command_output = interpret_command_func(user_input, self.distro_info, self.user_info)
                
                command = command_output.command
                notes = command_output.notes
                requires_sudo = command_output.requires_sudo
                
                # Add sudo warning to notes if needed
                if requires_sudo:
                    if notes:
                        notes = f"This command requires sudo privileges. {notes}"
                    else:
                        notes = "This command requires sudo privileges."
                
                # Display interpreted command
                help_info = {
                    'description': command_output.help.description,
                    'parameters': command_output.help.parameters,
                    'examples': command_output.help.examples,
                    'risks': command_output.help.risks,
                    'alternatives': command_output.help.alternatives,
                    'related_commands': command_output.help.related_commands,
                    'risk_score': command_output.help.risk_score
                } if hasattr(command_output, 'help') and command_output.help else None
                
                self.print_interpreted_command(command, notes, requires_sudo, help_info)
                
                # Check if command is safe
                if not is_safe_command_func(command):
                    self.print_error("This command requires manual intervention for safety reasons.")
                    self.command_history.append((command, "blocked"))
                    continue
                
                # Ask for confirmation
                if requires_sudo:
                    proceed = Confirm.ask("⚠️ This command requires sudo privileges. Execute it?", default=False)
                else:
                    proceed = Confirm.ask("Execute this command?", default=True)
                
                if not proceed:
                    self.console.print("❌ Command cancelled.", style="dim")
                    self.command_history.append((command, "cancelled"))
                    continue
                
                # Execute command with loading animation
                with self.console.status("[bold green]⚡ Executing command...", spinner="dots"):
                    result = execute_command_func(command, self.user_info)
                
                # Display results
                self.print_execution_result(result, command)
                
                # Add to history
                status = "success" if (isinstance(result, dict) and result.get('returncode') == 0) or (not isinstance(result, dict) and "error" not in str(result).lower()) else "error"
                self.command_history.append((command, status))
                
            except KeyboardInterrupt:
                self.console.print("\n👋 Goodbye! Thanks for using Shell Assistant!", style="bold blue")
                break
            except Exception as e:
                self.print_error(f"An error occurred: {str(e)}")
                if 'command' in locals():
                    self.command_history.append((command, "error"))
                continue
            
            self.console.print()  # Add spacing between commands 