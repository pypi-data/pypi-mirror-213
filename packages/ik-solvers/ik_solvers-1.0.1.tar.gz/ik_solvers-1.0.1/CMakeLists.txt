cmake_minimum_required(VERSION 3.14)
project(ik_solvers)

## Compile as C++11
add_compile_options(-std=c++11)

set(ADDITIONAL_COMPILE_OPTIONS -Wall -Wextra -Wpedantic -Wno-unused-parameter)

add_compile_options(${ADDITIONAL_COMPILE_OPTIONS})

find_package (Eigen3 3.3 REQUIRED NO_MODULE)

# Get pybind11 with FetchContent
include(FetchContent)

FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG        v2.10.1
)

FetchContent_MakeAvailable(pybind11)

set(LIB_SOURCE_FILES
  src/IKSolver.cpp
  src/ForwardDynamicsSolver.cpp
)
set(LIB_HEADER_FILES
  include/Utility.h
  include/IKSolver.h
  include/ForwardDynamicsSolver.h
  include/kdl_parser.hpp
)
add_subdirectory(lib/urdf_parser)
add_subdirectory(lib/orocos_kdl)

get_target_property(KDL_HEADERS orocos-kdl PUBLIC_HEADER)
file(GLOB KDL_UTIL_HPPS ${orocos_kdl_SOURCE_DIR}/src/utilities/[^.]*.h ${orocos_kdl_SOURCE_DIR}/src/utilities/[^.]*.hpp)

file(COPY ${KDL_HEADERS} DESTINATION ${orocos_kdl_BINARY_DIR}/include/kdl)
file(COPY ${KDL_UTIL_HPPS} DESTINATION ${orocos_kdl_BINARY_DIR}/include/kdl/utilities)

pybind11_add_module(PyIKSolver
${LIB_SOURCE_FILES} 
${LIB_HEADER_FILES}
src/pybindings.cpp
)
target_include_directories(PyIKSolver PRIVATE
include 
${EIGEN3_INCLUDE_DIR}
${PYBIND11_INCLUDE_DIR} 
${orocos_kdl_BINARY_DIR}/include
)

target_link_libraries(PyIKSolver PRIVATE
urdf_parser
orocos-kdl
)

get_target_property(inc_dirs PyIKSolver INCLUDE_DIRECTORIES)
message("INCLUDE_DIRECTORIES = ${inc_dirs}")

# message(orocos_kdl_lib = ${orocos_kdl_BINARY_DIR})
# message(orocos_kdl_headers = ${KDL_HEADERS})
# configure_file(${KDL_HEADERS} ${orocos_kdl_BINARY_DIR}/include/kdl COPYONLY)
# message(orocos_kdl_SOURCE_DIR = ${orocos_kdl_SOURCE_DIR})



