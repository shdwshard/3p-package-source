#!/bin/bash
#
# Script to use pre-compiled OpenSSL package instead of building from source
#

# Create a log file to track execution
exec > >(tee -a "/tmp/use_precompiled_openssl.log") 2>&1
echo "Starting use_precompiled_openssl.sh at $(date)"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." >/dev/null 2>&1 && pwd)"
OPENSSL_PACKAGE_DIR="$REPO_ROOT/3p-package-source/packages"
OPENSSL_PACKAGE=$(find "$OPENSSL_PACKAGE_DIR" -name "OpenSSL-*-mac-arm64.tar.xz" | head -n 1)

if [ -z "$OPENSSL_PACKAGE" ]; then
    echo "Could not find OpenSSL package in $OPENSSL_PACKAGE_DIR"
    exit 1
fi

echo "Using OpenSSL package: $OPENSSL_PACKAGE"

# Extract the OpenSSL package to a temporary directory
TEMP_DIR="$SCRIPT_DIR/temp/openssl_temp"
mkdir -p "$TEMP_DIR"
tar -xf "$OPENSSL_PACKAGE" -C "$TEMP_DIR"

# Get the Python framework directory
PYTHON_FRAMEWORK_DIR="$SCRIPT_DIR/temp/python_build/_root/Library/Frameworks/Python.framework"

# Create the necessary directories
mkdir -p "$PYTHON_FRAMEWORK_DIR/Versions/3.10/include"
mkdir -p "$PYTHON_FRAMEWORK_DIR/Versions/3.10/lib"

# Copy the OpenSSL headers and libraries to the framework directory
cp -R "$TEMP_DIR/OpenSSL/include/openssl" "$PYTHON_FRAMEWORK_DIR/Versions/3.10/include/"
cp "$TEMP_DIR/OpenSSL/lib/"*.dylib "$PYTHON_FRAMEWORK_DIR/Versions/3.10/lib/"

# Also copy to the build directory where Python's setup.py will look for it
# Try multiple possible locations
for BUILD_DIR in \
    "$SCRIPT_DIR/temp/python_build/_bld/openssl-1.1.1u-universal/arm64" \
    "$SCRIPT_DIR/temp/python_build/_bld/openssl-1.1.1u" \
    "$SCRIPT_DIR/temp/python_build/_bld/openssl-1.1.1t-universal/arm64" \
    "$SCRIPT_DIR/temp/python_build/_bld/openssl-1.1.1t" \
    "$SCRIPT_DIR/temp/python_build/_bld/openssl-universal/arm64" \
    "$SCRIPT_DIR/temp/python_build/_bld/openssl"
do
    if [ -d "$BUILD_DIR" ]; then
        echo "Copying OpenSSL files to $BUILD_DIR"
        mkdir -p "$BUILD_DIR/include"
        mkdir -p "$BUILD_DIR/lib"
        cp -R "$TEMP_DIR/OpenSSL/include/openssl" "$BUILD_DIR/include/"
        cp "$TEMP_DIR/OpenSSL/lib/"*.dylib "$BUILD_DIR/lib/"
    fi
done

# Also copy to the source directory
for SRC_DIR in \
    "$SCRIPT_DIR/temp/python_build/_src/openssl-1.1.1u" \
    "$SCRIPT_DIR/temp/python_build/_src/openssl-1.1.1t" \
    "$SCRIPT_DIR/temp/python_build/_src/openssl"
do
    if [ -d "$SRC_DIR" ]; then
        echo "Copying OpenSSL files to $SRC_DIR"
        mkdir -p "$SRC_DIR/include"
        mkdir -p "$SRC_DIR/lib"
        cp -R "$TEMP_DIR/OpenSSL/include/openssl" "$SRC_DIR/include/"
        cp "$TEMP_DIR/OpenSSL/lib/"*.dylib "$SRC_DIR/lib/"
    fi
done

# Also copy to the Python lib directory where modules will look for it
mkdir -p "$PYTHON_FRAMEWORK_DIR/Versions/3.10/lib/python3.10/lib-dynload"
cp "$TEMP_DIR/OpenSSL/lib/"*.dylib "$PYTHON_FRAMEWORK_DIR/Versions/3.10/lib/python3.10/lib-dynload/"

# Clean up
rm -rf "$TEMP_DIR"

echo "Successfully copied OpenSSL files to Python framework"
exit 0
