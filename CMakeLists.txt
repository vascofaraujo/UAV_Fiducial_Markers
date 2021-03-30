cmake_minimum_required(VERSION )
project(UAV-ART)
find_package(Opencv REQUIRED)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED)

include_directories($(OpenCV_INCLUDE_DIRS))
add_executable(UAV-ART main.cpp)
target_link_libraries(UAV-ART $(OpenCV_LIBS))