cmake_minimum_required(VERSION 3.0 FATAL_ERROR)

project(auto-ants.pp CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

function(set_policy POL VAL)
    if(POLICY ${POL})
        cmake_policy(SET ${POL} ${VAL})
    endif()
endfunction(set_policy)

set_policy(CMP0054 NEW) # ENABLE CMP0054: Only interpret if() arguments as variables or keywords when unquoted.
set_policy(CMP0058 NEW)
set_policy(CMP0042 NEW) # ENABLE CMP0042: MACOSX_RPATH is enabled by default.
set_policy(CMP0063 NEW) # ENABLE CMP0063: Honor visibility properties for all target types.
set_policy(CMP0077 NEW) # ENABLE CMP0077: option() honors normal variables

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

include(Dependencies)

add_subdirectory(src)
