#!/bin/bash
#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
# 
# SPDX-License-Identifier: Apache-2.0 OR MIT
#
#

# Modify the pngpriv.h file to avoid including fp.h on macOS
sed -i '' 's/#      include <fp.h>/#      include <math.h>/' $TEMP_FOLDER/src/pngpriv.h

# Configure the build
cmake -S $TEMP_FOLDER/src -B $TEMP_FOLDER/build -G Ninja \
    -DCMAKE_MACOSX_BUNDLE=OFF \
    -DCMAKE_TOOLCHAIN_FILE=../../../../Scripts/cmake/Platform/Mac/Toolchain_mac.cmake \
    -DCMAKE_APPLE_SILICON_PROCESSOR=arm64 \
    -DCMAKE_TOOLCHAIN_PLATFORM_NAME=Mac-arm64 \
    -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
    -DCMAKE_BUILD_TYPE=Release \
    -DPNG_SHARED=OFF \
    -DPNG_TESTS=OFF \
    -DPNG_DEBUG=OFF \
    -DPNG_STATIC=ON \
    -DCMAKE_POSITION_INDEPENDENT_CODE=TRUE \
    -DCMAKE_CXX_STANDARD=17 \
    -DBUILD_SHARED_LIBS=OFF \
    -DPNG_ARM_NEON=off \
    -DCMAKE_MODULE_PATH=$TEMP_FOLDER/zlib-1.2.11-rev5-mac-arm64 \
    -DCMAKE_INSTALL_PREFIX=$TEMP_FOLDER/working_install || exit 1

# Build the project
cmake --build $TEMP_FOLDER/build --config Release --parallel || exit 1

# Install the project
cmake --install $TEMP_FOLDER/build --config Release || exit 1

exit 0