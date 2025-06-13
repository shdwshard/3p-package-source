#!/usr/bin/env python3
"""
Script to modify the Python build-installer.py file to skip building OpenSSL.
"""
import os
import re

def modify_build_installer():
    # Path to the build-installer.py file
    script_dir = os.path.dirname(os.path.realpath(__file__))
    build_installer_path = os.path.join(script_dir, 'temp', 'cpython', 'Mac', 'BuildScript', 'build-installer.py')
    
    # Read the original file
    with open(build_installer_path, 'r') as f:
        content = f.read()
    
    # Find the OpenSSL recipe in the library_recipes function
    pattern = r'(result\.append\(dict\(\s*name="OpenSSL[^}]*?buildrecipe=build_universal_openssl[^}]*?\),\s*)'
    
    # Add a return statement after the OpenSSL recipe
    replacement = r'\1\n        # Skip building other dependencies - we only need OpenSSL\n        return result\n\n'
    
    # Replace in the content
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Write the modified content back to the file
    with open(build_installer_path, 'w') as f:
        f.write(new_content)
    
    print(f"Successfully modified {build_installer_path} to skip building dependencies after OpenSSL")
    return True

if __name__ == "__main__":
    if modify_build_installer():
        exit(0)
    else:
        exit(1)