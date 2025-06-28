#!/usr/bin/env python3
"""
Test script to demonstrate the new risk scoring feature
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ollama_interface import interpret_command
from distro_detector import get_distro_info
from user_info import get_user_info

def test_risk_scoring():
    """Test the risk scoring feature with various commands"""
    
    # Get system information
    distro_info = get_distro_info()
    user_info = get_user_info()
    
    print("🚀 Testing Risk Scoring Feature")
    print("=" * 60)
    print(f"System: {distro_info}")
    print(f"User: {user_info['username']}")
    print()
    
    # Test commands with different risk levels
    test_commands = [
        # Safe commands (0-2)
        "show me the current date",
        "list files in current directory",
        "show disk usage",
        
        # Low risk commands (3-4)
        "create a new file called test.txt",
        "copy a file to another location",
        "find all text files",
        
        # Medium risk commands (5-6)
        "check network connectivity",
        "show system processes",
        "search for files containing text",
        
        # High risk commands (7-8)
        "install a package",
        "modify system settings",
        "change file permissions",
        
        # Extreme risk commands (9-10)
        "delete all files in home directory",
        "format the hard drive",
        "remove system files"
    ]
    
    for i, command in enumerate(test_commands, 1):
        print(f"Test {i}: {command}")
        print("-" * 50)
        
        try:
            result = interpret_command(command, distro_info, user_info)
            
            print(f"Command: {result.command}")
            print(f"Requires sudo: {result.requires_sudo}")
            print(f"Notes: {result.notes}")
            
            # Display risk score with color coding
            risk_score = result.help.risk_score
            risk_level = get_risk_level(risk_score)
            print(f"Risk Score: {risk_score}/10 - {risk_level}")
            
            print(f"Description: {result.help.description}")
            
            if result.help.risks:
                print("Risks:")
                for risk in result.help.risks:
                    print(f"  • {risk}")
            
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n" + "=" * 60 + "\n")

def get_risk_level(risk_score: int) -> str:
    """Get risk level description based on risk score"""
    if risk_score <= 2:
        return "🟢 Safe"
    elif risk_score <= 4:
        return "🟡 Low Risk"
    elif risk_score <= 6:
        return "🟠 Medium Risk"
    elif risk_score <= 8:
        return "🔴 High Risk"
    else:
        return "⛔ Extreme Risk"

if __name__ == "__main__":
    test_risk_scoring() 