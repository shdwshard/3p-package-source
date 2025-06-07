
#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
# 
# SPDX-License-Identifier: Apache-2.0 OR MIT
#
#

# this file just exists to provide a place to put defaults that should be present 
# in all 3p packages so that they don't have to seperately define this for each one.

set(CMAKE_SYSTEM_NAME Darwin)
set(CMAKE_OSX_DEPLOYMENT_TARGET "11.0" CACHE STRING "The minimum OSX Version to support" FORCE)
set(CMAKE_POSITION_INDEPENDENT_CODE TRUE)

# If we need to compile for Mac M1, set CMAKE_APPLE_SILICON_PROCESSOR to arm64 on the command line.
# this will override CMAKE_HOST_SYSTEM_PROCESSOR.
# Check if the platform name contains "arm64" and set CMAKE_APPLE_SILICON_PROCESSOR accordingly
if(DEFINED CMAKE_TOOLCHAIN_PLATFORM_NAME AND CMAKE_TOOLCHAIN_PLATFORM_NAME MATCHES ".*arm64.*")
    set(CMAKE_APPLE_SILICON_PROCESSOR "arm64")
endif()

# For Mac-arm64 platform, we need to explicitly set CMAKE_APPLE_SILICON_PROCESSOR
# Check if the platform name is passed via -DCMAKE_TOOLCHAIN_PLATFORM_NAME
if(NOT DEFINED CMAKE_APPLE_SILICON_PROCESSOR)
    # If not explicitly set, check if we're running on Apple Silicon
    execute_process(
        COMMAND uname -m
        OUTPUT_VARIABLE ARCH
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    if(ARCH STREQUAL "arm64")
        set(CMAKE_APPLE_SILICON_PROCESSOR "arm64")
    endif()
endif()

set(CMAKE_SYSTEM_PROCESSOR ${CMAKE_HOST_SYSTEM_PROCESSOR})

# Add compiler definitions to fix zlib build issues
if(CMAKE_APPLE_SILICON_PROCESSOR STREQUAL "arm64")
    # Define OS_CODE to 7 to prevent redefinition in zutil.h
    # This matches the value set for MACOS/TARGET_OS_MAC
    add_compile_definitions(OS_CODE=7)

    # Prevent fdopen macro redefinition by defining it as itself
    # This ensures the system's fdopen function is used
    add_compile_definitions(fdopen=fdopen)
endif()

# cmake will auto-select the rest.
