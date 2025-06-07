#!/bin/bash
#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
# 
# SPDX-License-Identifier: Apache-2.0 OR MIT
#
#

# Create the target directories
mkdir -p $TARGET_INSTALL_ROOT/include
mkdir -p $TARGET_INSTALL_ROOT/lib

# Copy the license file
cp -f $TEMP_FOLDER/src/LICENSE $TARGET_INSTALL_ROOT/ || exit 1

# Copy the include files
cp -rf $TEMP_FOLDER/working_install/include/* $TARGET_INSTALL_ROOT/include/ || exit 1

# Copy the library files
cp -f $TEMP_FOLDER/working_install/lib/libpng*.a $TARGET_INSTALL_ROOT/lib/ || exit 1

exit 0