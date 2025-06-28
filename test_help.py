#!/usr/bin/env python3
"""
Test script to demonstrate the new contextual help feature
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ollama_interface import interpret_command
from distro_detector import get_distro_info
from user_info import get_user_info

def test_help_feature():
    """Test the contextual help feature with various commands"""
    
    # Get system information
    distro_info = get_distro_info()
    user_info = get_user_info()
    
    print("🚀 Testing Contextual Help Feature")
    print("=" * 50)
    print(f"System: {distro_info}")
    print(f"User: {user_info['username']}")
    print()
    
    # Test commands
    test_commands = [
        "show me disk usage",
        "find all Python files in my home directory",
        "check system status",
        "list running processes",
        "search for text in files"
    ]
    
    for i, command in enumerate(test_commands, 1):
        print(f"Test {i}: {command}")
        print("-" * 30)
        
        try:
            result = interpret_command(command, distro_info, user_info)
            
            print(f"Command: {result.command}")
            print(f"Requires sudo: {result.requires_sudo}")
            print(f"Notes: {result.notes}")
            print()
            
            # Display help information
            help_info = result.help
            print("📖 Detailed Help:")
            print(f"Description: {help_info.description}")
            
            if help_info.parameters:
                print(f"Parameters: {', '.join(help_info.parameters)}")
            
            if help_info.examples:
                print("Examples:")
                for example in help_info.examples:
                    print(f"  • {example}")
            
            if help_info.risks:
                print("Risks:")
                for risk in help_info.risks:
                    print(f"  • {risk}")
            
            if help_info.alternatives:
                print("Alternatives:")
                for alt in help_info.alternatives:
                    print(f"  • {alt}")
            
            if help_info.related_commands:
                print("Related Commands:")
                for cmd in help_info.related_commands:
                    print(f"  • {cmd}")
            
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    test_help_feature() 