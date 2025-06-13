#!/usr/bin/env python3
"""
Script to modify the Python build-installer.py file to force using the older TCL version (8.6.8).
"""
import os
import re

def force_old_tcl():
    # Path to the build-installer.py file
    script_dir = os.path.dirname(os.path.realpath(__file__))
    build_installer_path = os.path.join(script_dir, 'temp', 'cpython', 'Mac', 'BuildScript', 'build-installer.py')
    
    # Read the original file
    with open(build_installer_path, 'r') as f:
        content = f.read()
    
    # Find the useOldTk function
    pattern = r'def useOldTk\(\):\s*return getBuildTuple\(\) < \(10, 15\)'
    
    # Replace it to always return True
    replacement = r'def useOldTk():\n    return True  # Always use older TCL version (8.6.8) to avoid download issues'
    
    # Replace in the content
    new_content = re.sub(pattern, replacement, content)
    
    # Write the modified content back to the file
    with open(build_installer_path, 'w') as f:
        f.write(new_content)
    
    print(f"Successfully modified {build_installer_path} to always use the older TCL version (8.6.8)")
    return True

if __name__ == "__main__":
    if force_old_tcl():
        exit(0)
    else:
        exit(1)