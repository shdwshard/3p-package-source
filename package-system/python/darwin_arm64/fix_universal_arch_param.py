#!/usr/bin/env python3
"""
Script to fix the universal arch parameter in the Python build-installer.py file.
"""
import os
import re

def fix_universal_arch_param():
    # Path to the build-installer.py file
    script_dir = os.path.dirname(os.path.realpath(__file__))
    build_installer_path = os.path.join(script_dir, 'temp', 'cpython', 'Mac', 'BuildScript', 'build-installer.py')

    # Read the original file
    with open(build_installer_path, 'r') as f:
        content = f.read()

    # Fix the parameter name from --with-universal-arch to --with-universal-archs
    pattern = r'--with-universal-arch=%s'
    replacement = r'--with-universal-archs=%s'

    # Replace in the content
    new_content = re.sub(pattern, replacement, content)

    # Write the modified content back to the file
    with open(build_installer_path, 'w') as f:
        f.write(new_content)

    print(f"Successfully fixed universal arch parameter in {build_installer_path}")
    return True

if __name__ == "__main__":
    if fix_universal_arch_param():
        exit(0)
    else:
        exit(1)
