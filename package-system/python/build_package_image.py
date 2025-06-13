#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
# 
# SPDX-License-Identifier: Apache-2.0 OR MIT
#
#

# this script builds python for linux and darwin_x64
# and places the result in linux_x64/package or darwin_x64/package 
import subprocess
import sys
import os
import platform

folder_names = { #   subfolder     interpreter     build script 
    'darwin'        : ('darwin_x64' , 'Python.framework/Versions/3.10/bin/python3', 'make-python.sh'),
    'linux'         : ('linux_x64'  , 'python/bin/python', 'make-python.sh'),
    'windows'       : ('win_x64'    , 'python/python.exe', 'build_python.bat')
}

# Add support for platform-specific builds
platform_specific_folder_names = {
    'mac-arm64'     : ('darwin_arm64', 'Python.framework/Versions/3.10/bin/python3', 'make-python.sh')
}

import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description='Build Python package')
parser.add_argument('--platform', dest='platform', help='Platform to build for (e.g., mac-arm64)')
args, unknown = parser.parse_known_args()

if args.platform and args.platform in platform_specific_folder_names:
    # Use platform-specific folder names
    subfolder_name, binary_relpath, build_script = platform_specific_folder_names[args.platform]
else:
    # Use default folder names based on system
    platformsys = platform.system().lower()
    # For linux, we may support aarch64 architecture as well as the default x86_64
    if platformsys == 'linux' and platform.machine() == 'aarch64':
        print("Linux aarch64 builds not supported by this script")
        sys.exit(1)

    # intentionally generate a keyerror if its not a good platform:
    subfolder_name, binary_relpath, build_script = folder_names[platformsys]

script_dir = os.path.dirname(os.path.realpath(__file__))
build_script_dir = os.path.join(script_dir, subfolder_name)
test_script_name = os.path.join(script_dir, 'quick_validate_python.py')
build_script_name = os.path.join(build_script_dir, build_script)

# the built python is expected to be in build script dir/package/...
python_dir = os.path.join(build_script_dir, 'package' )
python_executable = os.path.join(python_dir, binary_relpath)

# build python using the build script
result_value = subprocess.run([build_script_name], shell=True, cwd=build_script_dir)

if result_value.returncode != 0:
    sys.exit(result_value.returncode)

# test out the freshly created python executable:
result_value = subprocess.run([python_executable, test_script_name], cwd=python_dir)
sys.exit(result_value.returncode)
