cmake_minimum_required(VERSION 3.0.2)
project(ceva)

## Compile as C++11, supported in ROS Kinetic and newer
set(CMAKE_BUILD_TYPE "Release")
set(CMAKE_CXX_FLAGS "-std=c++17 -Wfatal-errors")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -Wall -g")

find_package(
  catkin REQUIRED COMPONENTS
  pybind11_catkin
)

catkin_python_setup()

# Needed non-ros packages
find_package(OpenMP REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(fmt REQUIRED)

catkin_package(
  LIBRARIES
  CATKIN_DEPENDS pybind11_catkin
)

include_directories(
  ${PROJECT_SOURCE_DIR}/include
  ${catkin_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIR}
)

pybind_add_module(
  ceva MODULE src/ceva.cpp
)

# Link the module with libraries
target_link_libraries(
  ceva PRIVATE fmt::fmt Eigen3::Eigen ${OpenMP_CXX_FLAGS} ${catkin_LIBRARIES}
)

# catkin_install_python(
#   PROGRAMS scripts/test.py DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
# )

install(
  TARGETS ceva LIBRARY DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
