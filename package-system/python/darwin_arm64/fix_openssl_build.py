#!/usr/bin/env python3
"""
Script to fix the OpenSSL build process to skip i386 architecture on ARM64 Macs.
"""
import os
import re
import platform

def fix_openssl_build():
    # Path to the build-installer.py file
    script_dir = os.path.dirname(os.path.realpath(__file__))
    build_installer_path = os.path.join(script_dir, 'temp', 'cpython', 'Mac', 'BuildScript', 'build-installer.py')

    # Read the original file
    with open(build_installer_path, 'r') as f:
        content = f.read()

    # Check if we're on an ARM64 Mac
    is_arm64 = platform.machine() == 'arm64'

    if is_arm64:
        # Modify the build_universal_openssl function to skip i386 architecture
        pattern = r"(def build_universal_openssl\(basedir, archList\):.*?for arch in archList:)"
        replacement = r"\1\n        # Skip i386 architecture on ARM64 Macs\n        if arch == 'i386':\n            continue"

        # Replace in the content
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        # Write the modified content back to the file
        with open(build_installer_path, 'w') as f:
            f.write(new_content)

        print(f"Successfully modified {build_installer_path} to skip i386 architecture on ARM64 Macs")
    else:
        print(f"Not on an ARM64 Mac, no need to modify {build_installer_path}")

    return True

if __name__ == "__main__":
    if fix_openssl_build():
        exit(0)
    else:
        exit(1)