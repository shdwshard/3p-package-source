#!/bin/bash
#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#
#

rm -rf temp/build_test
mkdir temp/build_test

cmake -S test -B temp/build_test -G Xcode \
 -DCMAKE_TOOLCHAIN_FILE=../../../../Scripts/cmake/Platform/Mac/Toolchain_mac.cmake \
 -DCMAKE_MODULE_PATH="$PACKAGE_ROOT" || exit 1

cmake --build temp/build_test --parallel --config Release || exit 1

temp/build_test/Release/test_OpenSSL "OpenSSL 1.1.1t  7 Feb 2023" "e9a3e92b2d1496d551fa6ec7e173e0494c1a9e7f" > test_output.log 2>&1 || { cat test_output.log; exit 1; }

exit 0
