######## A simple cmakelists.txt file for OpenCV() #############  
cmake_minimum_required(VERSION 2.8)                            
PROJECT(alt)                                         

FIND_PACKAGE( OpenCV REQUIRED )                              
INCLUDE_DIRECTORIES( ${OpenCV_INCLUDE_DIRS} )

ADD_EXECUTABLE(alt1 alt1_cpp.cpp)                         
TARGET_LINK_LIBRARIES (alt1 ${OpenCV_LIBS})         
########### end ####################################  