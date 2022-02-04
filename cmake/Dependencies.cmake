
find_package(Boost REQUIRED)
find_library(SPICY spicy)
message(STATUS "VIP ${SPICY}")

include(CPM)

CPMAddPackage(
  GITHUB_REPOSITORY "mfontanini/libtins"
  VERSION 4.3
  OPTIONS
    "LIBTINS_BUILD_EXAMPLES OFF"
    "LIBTINS_BUILD_TESTS OFF"
    "LIBTINS_ENABLE_CXX11 ON"
    "LIBTINS_BUILD_SHARED ${BUILD_SHARED_LIBS}"
)

if(libtins_ADDED)
  add_library(libtins INTERFACE IMPORTED)
  target_include_directories(libtins INTERFACE "${libtins_SOURCE_DIR}/include")
  target_link_libraries(libtins INTERFACE tins)
  set_target_properties(libtins PROPERTIES CXX_STANDARD 11)
endif()

# TODO: GUI

# set(NANOGUI_FLAGS "")
# if ("${CMAKE_CXX_COMPILER_ID}" MATCHES "Clang")
#   set(NANOGUI_FLAGS "-mcpu=native")
# elseif (CMAKE_COMPILER_IS_GNUCXX)
#   set(NANOGUI_FLAGS "-march=native")
# endif()

# CPMAddPackage(
#   GITHUB_REPOSITORY psdpp/nanogui
#   GIT_TAG master
#   OPTIONS
#     "NANOGUI_BUILD_EXAMPLES OFF"
#     "NANOGUI_BUILD_PYTHON OFF"
#     "NANOGUI_NATIVE_FLAGS ${NANOGUI_FLAGS}"
#     "NANOGUI_BUILD_SHARED ${BUILD_SHARED_LIBS}"
# )
# if(nanogui_ADDED AND CMAKE_COMPILER_IS_GNUCXX)
#   remove_flag_from_target(nanogui "-Werror")
#   remove_flag_from_target(glfw_objects "-Wpedantic")
# endif()
