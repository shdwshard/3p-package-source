#!/usr/bin/env python3
"""
Script to fix library warnings in the Python build-installer.py file.
"""
import os
import re

def fix_library_warnings():
    # Path to the build-installer.py file
    script_dir = os.path.dirname(os.path.realpath(__file__))
    build_installer_path = os.path.join(script_dir, 'temp', 'cpython', 'Mac', 'BuildScript', 'build-installer.py')
    setup_path = os.path.join(script_dir, 'temp', 'cpython', 'Modules', 'Setup')

    # Read the original file
    with open(build_installer_path, 'r') as f:
        content = f.read()

    # Find the configure command
    pattern = r'runCommand\("%s -C --enable-framework --enable-universalsdk=/ '
    pattern += r'"--with-universal-archs=%s "'
    pattern += r'"%s "'
    pattern += r'"%s "'
    pattern += r'"%s "'
    pattern += r'"%s "'
    pattern += r'"%s "'
    pattern += r'"%s "'
    pattern += r'"LDFLAGS=\'-g -L%s/libraries/usr/local/lib\' "'
    pattern += r'"CFLAGS=\'-g -I%s/libraries/usr/local/include\' 2>&1"%\('

    # Add the --with-dbmliborder option to exclude gdbm
    replacement = r'runCommand("%s -C --enable-framework --enable-universalsdk=/ '
    replacement += r'"--with-universal-archs=%s "'
    replacement += r'"%s "'
    replacement += r'"%s "'
    replacement += r'"%s "'
    replacement += r'"%s "'
    replacement += r'"%s "'
    replacement += r'"%s "'
    replacement += r'"--with-dbmliborder=ndbm:bdb "'
    replacement += r'"LDFLAGS=\'-g -L%s/libraries/usr/local/lib\' "'
    replacement += r'"CFLAGS=\'-g -I%s/libraries/usr/local/include\' 2>&1"%('

    # Replace in the content
    new_content = re.sub(pattern, replacement, content)

    # Write the modified content back to the file
    with open(build_installer_path, 'w') as f:
        f.write(new_content)

    print(f"Successfully added --with-dbmliborder=ndbm:bdb to {build_installer_path}")

    # Now modify the Setup file to disable the uuid module
    with open(setup_path, 'r') as f:
        setup_content = f.read()

    # Check if the *disabled* section exists
    if '*disabled*' in setup_content:
        # Add _uuid to the list of disabled modules
        disabled_pattern = r'#\*disabled\*\n#\n#(.*)'
        disabled_replacement = r'#*disabled*\n#\n#\1 _uuid'
        setup_content = re.sub(disabled_pattern, disabled_replacement, setup_content)
    else:
        # If there's no *disabled* section, add it at the end
        setup_content += '\n#*disabled*\n#\n#_uuid\n'

    # Write the modified content back to the file
    with open(setup_path, 'w') as f:
        f.write(setup_content)

    print(f"Successfully disabled _uuid module in {setup_path}")
    return True

if __name__ == "__main__":
    if fix_library_warnings():
        exit(0)
    else:
        exit(1)
