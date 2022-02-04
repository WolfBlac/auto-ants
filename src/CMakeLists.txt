
include(GNUInstallDirs)

file(GLOB SOURCES *.hpp *.cpp)

add_executable(autoantspp ${SOURCES})

target_link_libraries(autoantspp
  PRIVATE
    ${SPICY}
    libtins
    Boost::boost)

install(
  TARGETS autoantspp RUNTIME
  DESTINATION ${CMAKE_INSTALL_BINDIR}
)
