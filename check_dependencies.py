#!/usr/bin/env python3
"""
Dependency checker for Shell Assistant
Checks if all required packages are installed and returns appropriate exit codes
"""

import sys
import importlib
import pkg_resources

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = {
        'Flask': '3.0.0',
        'ollama': '0.1.7', 
        'pydantic': '2.5.0',
        'colorama': '0.4.6',
        'rich': '13.7.0'
    }
    
    missing_packages = []
    outdated_packages = []
    
    for package, required_version in required_packages.items():
        try:
            # Try to import the package
            importlib.import_module(package.lower())
            
            # Check version if specified
            try:
                installed_version = pkg_resources.get_distribution(package).version
                if pkg_resources.parse_version(installed_version) < pkg_resources.parse_version(required_version):
                    outdated_packages.append(f"{package} (installed: {installed_version}, required: {required_version})")
            except pkg_resources.DistributionNotFound:
                # Package is installed but version can't be determined
                pass
                
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        return 1
    
    if outdated_packages:
        print(f"Outdated packages: {', '.join(outdated_packages)}")
        return 2
    
    print("All dependencies are satisfied!")
    return 0

if __name__ == "__main__":
    exit_code = check_dependencies()
    sys.exit(exit_code) 