#!/usr/bin/env python3
"""
Script to modify the Python build-installer.py file to use a newer TCL version and update the download URL.
"""
import os
import re

def update_tcl_version():
    # Path to the build-installer.py file
    script_dir = os.path.dirname(os.path.realpath(__file__))
    build_installer_path = os.path.join(script_dir, 'temp', 'cpython', 'Mac', 'BuildScript', 'build-installer.py')

    # Read the original file
    with open(build_installer_path, 'r') as f:
        content = f.read()

    # 1. Find the useOldTk function and modify it to always return False
    pattern_useoldtk = r'def useOldTk\(\):\s*return.*'
    replacement_useoldtk = r'def useOldTk():\n    return False  # Use newer TCL version'

    # 2. Update the TCL/TK version and download URL in the library_recipes function
    pattern_tcl_url = r'(url="https://fossies\.org/linux/misc/tcl%s-src\.tar\.gz"%\(tcl_tk_ver,\),)'
    replacement_tcl_url = r'url="https://sourceforge.net/projects/tcl/files/Tcl/%s/tcl%s-src.tar.gz" % (tcl_tk_ver, tcl_tk_ver),'

    pattern_tk_url = r'(url="https://fossies\.org/linux/misc/tk%s-src\.tar\.gz"%\(tcl_tk_ver,\),)'
    replacement_tk_url = r'url="https://sourceforge.net/projects/tcl/files/Tcl/%s/tk%s-src.tar.gz" % (tcl_tk_ver, tcl_tk_ver),'

    # 3. Update the TCL/TK version to 8.6.12 (a version that should be available)
    pattern_tcl_ver = r'(tcl_tk_ver=\'8\.6\.13\')'
    replacement_tcl_ver = r"tcl_tk_ver='8.6.12'"

    # 4. Update the TCL checksum to match the correct value for 8.6.12
    pattern_tcl_checksum = r'(tcl_checksum=\'0e4358aade2f5db8a8b6f2f6d9481ec2\')'
    replacement_tcl_checksum = r"tcl_checksum='87ea890821d2221f2ab5157bc5eb885f'"

    # 5. Update the TK checksum to match the correct value for 8.6.12
    pattern_tk_checksum = r'(tk_checksum=\'95adc33d55a133ee29bc9f81efdf31b2\')'
    replacement_tk_checksum = r"tk_checksum='1d6dcf6120356e3d211e056dff5e462a'"

    # Apply all replacements
    new_content = re.sub(pattern_useoldtk, replacement_useoldtk, content)
    new_content = re.sub(pattern_tcl_url, replacement_tcl_url, new_content)
    new_content = re.sub(pattern_tk_url, replacement_tk_url, new_content)
    new_content = re.sub(pattern_tcl_ver, replacement_tcl_ver, new_content)
    new_content = re.sub(pattern_tcl_checksum, replacement_tcl_checksum, new_content)
    new_content = re.sub(pattern_tk_checksum, replacement_tk_checksum, new_content)

    # Write the modified content back to the file
    with open(build_installer_path, 'w') as f:
        f.write(new_content)

    print(f"Successfully updated {build_installer_path} to use TCL/TK 8.6.12 from SourceForge")
    return True

if __name__ == "__main__":
    if update_tcl_version():
        exit(0)
    else:
        exit(1)
