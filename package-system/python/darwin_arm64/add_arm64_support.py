#!/usr/bin/env python3
"""
Script to add arm64 support to the Python build-installer.py file.
"""
import os
import re

def add_arm64_support():
    # Path to the build-installer.py file
    script_dir = os.path.dirname(os.path.realpath(__file__))
    build_installer_path = os.path.join(script_dir, 'temp', 'cpython', 'Mac', 'BuildScript', 'build-installer.py')

    # Read the original file
    with open(build_installer_path, 'r') as f:
        content = f.read()

    # Add arm64 to universal_opts_map
    pattern_universal_opts = r'(universal_opts_map\s*=\s*\{[^}]*?\'all\':\s*\([^)]*?\),\s*\})'
    replacement_universal_opts = r'\1\n\n# Added arm64 support\nuniversal_opts_map["arm64"] = ("arm64",)'

    # Add arm64 to default_target_map
    pattern_default_target = r'(default_target_map\s*=\s*\{[^}]*?\'all\':\s*\'[^\']*\',\s*\})'
    replacement_default_target = r'\1\n\n# Added arm64 support\ndefault_target_map["arm64"] = "11.0"'

    # Update UNIVERSALOPTS to include arm64
    pattern_universalopts = r'(UNIVERSALOPTS\s*=\s*tuple\(universal_opts_map\.keys\(\)\))'
    replacement_universalopts = r'# Added arm64 support\nuniversal_opts_map["arm64"] = ("arm64",)\n\n\1'

    # Replace in the content
    new_content = re.sub(pattern_universal_opts, replacement_universal_opts, content, flags=re.DOTALL)
    new_content = re.sub(pattern_default_target, replacement_default_target, new_content, flags=re.DOTALL)
    new_content = re.sub(pattern_universalopts, replacement_universalopts, new_content, flags=re.DOTALL)

    # Write the modified content back to the file
    with open(build_installer_path, 'w') as f:
        f.write(new_content)

    print(f"Successfully added arm64 support to {build_installer_path}")
    return True

if __name__ == "__main__":
    if add_arm64_support():
        exit(0)
    else:
        exit(1)
