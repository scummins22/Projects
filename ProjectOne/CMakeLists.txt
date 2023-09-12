cmake_minimum_required(VERSION 3.26)
project(ProjectOne)

set(CMAKE_CXX_STANDARD 17)

add_executable(ProjectOne main.cpp
        Auditorium.h
        Auditorium.cpp
        Node.cpp
        Node.h
        Seat.cpp
        Seat.h)
