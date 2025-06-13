#!/usr/bin/env python3
"""
Script to modify the Python build-installer.py file to use pre-compiled OpenSSL.
"""
import os
import re
import shutil

def modify_build_installer():
    # Path to the build-installer.py file
    script_dir = os.path.dirname(os.path.realpath(__file__))
    build_installer_path = os.path.join(script_dir, 'temp', 'cpython', 'Mac', 'BuildScript', 'build-installer.py')

    # Read the original file
    with open(build_installer_path, 'r') as f:
        content = f.read()

    # Find the build_universal_openssl function
    pattern = r'def build_universal_openssl\(basedir, archList\):.*?(?=def )'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        print("Could not find build_universal_openssl function in build-installer.py")
        return False

    # Get the indentation of the original function
    original_lines = match.group(0).splitlines()
    if len(original_lines) > 1:
        # Find the indentation of the first non-empty line after the function definition
        for line in original_lines[1:]:
            if line.strip():
                indentation = re.match(r'^(\s*)', line).group(1)
                break
        else:
            indentation = '    '  # Default indentation if no non-empty lines found
    else:
        indentation = '    '  # Default indentation

    # Replacement function with proper indentation
    replacement = f'''def build_universal_openssl(basedir, archList):
{indentation}"""
{indentation}Special case build recipe for universal build of openssl.
{indentation}
{indentation}Instead of building OpenSSL from source, use the pre-compiled
{indentation}OpenSSL package from the O3DE package system.
{indentation}"""
{indentation}import glob
{indentation}import subprocess
{indentation}
{indentation}print("Using pre-compiled OpenSSL package instead of building from source")
{indentation}
{indentation}# Find the OpenSSL package in the packages directory
{indentation}repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../.."))
{indentation}openssl_package_dir = os.path.join(repo_root, "3p-package-source", "packages")
{indentation}openssl_package_pattern = os.path.join(openssl_package_dir, "OpenSSL-*-mac-arm64.tar.xz")
{indentation}openssl_packages = glob.glob(openssl_package_pattern)
{indentation}
{indentation}if not openssl_packages:
{indentation}{indentation}fatal("Could not find OpenSSL package in %s" % openssl_package_dir)
{indentation}
{indentation}openssl_package = openssl_packages[0]
{indentation}print("Using OpenSSL package: %s" % openssl_package)
{indentation}
{indentation}# Extract the OpenSSL package to a temporary directory
{indentation}temp_dir = os.path.join(os.path.dirname(basedir), "openssl_temp")
{indentation}os.makedirs(temp_dir, exist_ok=True)
{indentation}subprocess.run(["tar", "-xf", openssl_package, "-C", temp_dir], check=True)
{indentation}
{indentation}# Create the necessary directories in the basedir
{indentation}basefw = os.path.join(basedir, *FW_VERSION_PREFIX)
{indentation}os.makedirs(os.path.join(basefw, "include"), exist_ok=True)
{indentation}os.makedirs(os.path.join(basefw, "lib"), exist_ok=True)
{indentation}
{indentation}# Copy the OpenSSL headers and libraries to the basedir
{indentation}shutil.copytree(os.path.join(temp_dir, "OpenSSL", "include", "openssl"), os.path.join(basefw, "include", "openssl"))
{indentation}
{indentation}for lib in glob.glob(os.path.join(temp_dir, "OpenSSL", "lib", "*.dylib")):
{indentation}{indentation}shutil.copy(lib, os.path.join(basefw, "lib"))
{indentation}
{indentation}# Clean up
{indentation}shutil.rmtree(temp_dir)
'''

    # Replace the function in the content
    new_content = content.replace(match.group(0), replacement)

    # Write the modified content back to the file
    with open(build_installer_path, 'w') as f:
        f.write(new_content)

    print(f"Successfully modified {build_installer_path}")
    return True

if __name__ == "__main__":
    if modify_build_installer():
        exit(0)
    else:
        exit(1)
