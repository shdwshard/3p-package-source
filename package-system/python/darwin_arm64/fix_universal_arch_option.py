#!/usr/bin/env python3
"""
Script to fix the universal arch option in the Python build-installer.py file.
"""
import os
import re

def fix_universal_arch_option():
    # Path to the build-installer.py file
    script_dir = os.path.dirname(os.path.realpath(__file__))
    build_installer_path = os.path.join(script_dir, 'temp', 'cpython', 'Mac', 'BuildScript', 'build-installer.py')

    # Read the original file
    with open(build_installer_path, 'r') as f:
        content = f.read()

    # Fix the parameter name in the getopt.getopt call
    pattern = r"getopt\.getopt\(args, '[^']*',\s*\[\s*'[^']*',\s*'[^']*',\s*'[^']*'\s*,\s*'[^']*',\s*'universal-archs=',\s*'help'\s*\]\)"
    replacement = r"getopt.getopt(args, '?hb',\n                [ 'build-dir=', 'third-party=', 'sdk-path=' , 'src-dir=',\n                  'dep-target=', 'universal-archs=', 'universal-arch=', 'help' ])"

    # Replace in the content
    new_content = re.sub(pattern, replacement, content)

    # Fix the parameter name in the options processing
    pattern = r"(\s+elif k in \('--universal-archs', \):)\s*\n(\s+if v in UNIVERSALOPTS:)"
    replacement = r"\1\n            if v in UNIVERSALOPTS:\n                universal = v\n            else:\n                usage(1, 'Unknown universal architecture: %s' % v)\n        elif k in ('--universal-arch', ):\n\2"

    # Replace in the content
    new_content = re.sub(pattern, replacement, new_content, flags=re.DOTALL)

    # Write the modified content back to the file
    with open(build_installer_path, 'w') as f:
        f.write(new_content)

    print(f"Successfully fixed universal arch option in {build_installer_path}")
    return True

if __name__ == "__main__":
    if fix_universal_arch_option():
        exit(0)
    else:
        exit(1)
