cmake_minimum_required(VERSION 3.26)
project(Project3)

set(CMAKE_CXX_STANDARD 11)

add_executable(Project3 main.cpp
        BinTree.h
        Node.h
        DVD.h
        DVD.cpp
)

# Add compiler flags to the target
target_compile_options(Project3 PRIVATE
        -Wall              # Enable common warnings
        -Werror            # Treat warnings as errors
        -Wextra            # Enable extra warnings
        -Wuninitialized    # Warn about uninitialized variables
        -pedantic-errors   # Treat pedantic warnings as errors
        -Wconversion       # Warn about implicit type conversions
        # Add other flags here as needed
)