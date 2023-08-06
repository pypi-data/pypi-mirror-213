cmake_minimum_required(VERSION 3.15)

set(CMAKE_INSTALL_PREFIX "${CMAKE_BINARY_DIR}/artifacts" CACHE STRING "" FORCE)

include(FetchContent)

message("Fetching mongo-c-driver...")
FetchContent_Declare(mongocdriver
        GIT_REPOSITORY  "https://github.com/mongodb/mongo-c-driver.git"
        GIT_TAG         "1.23.2"
        )
FetchContent_GetProperties(mongocdriver)

if(NOT mongocdriver_POPULATED)
    set(ENABLE_MONGOC OFF CACHE BOOL "" FORCE)
    set(ENABLE_AUTOMATIC_INIT_AND_CLEANUP OFF CACHE BOOL "" FORCE)
    set(ENABLE_TESTS OFF CACHE BOOL "" FORCE)
    set(ENABLE_EXAMPLES OFF CACHE BOOL "" FORCE)

    FetchContent_Populate(mongocdriver)
    message("---> Mongo C driver source: ${mongocdriver_SOURCE_DIR}")
    message("---> Mongo C driver binaries: ${mongocdriver_BINARY_DIR}")

    add_subdirectory(  ${mongocdriver_SOURCE_DIR}  ${mongocdriver_BINARY_DIR} )
endif()

FetchContent_MakeAvailable(mongocdriver)

message("Fetching spdlog...")
FetchContent_Declare(spdlog
        GIT_REPOSITORY https://github.com/gabime/spdlog.git
        GIT_TAG        v1.10.0)

FetchContent_GetProperties(spdlog)
if(NOT spdlog_POPULATED)
    FetchContent_Populate(spdlog)
    message("---> spdlog source: ${spdlog_SOURCE_DIR}")
    message("---> spdlog: ${spdlog_BINARY_DIR}")
    add_subdirectory(${spdlog_SOURCE_DIR} ${spdlog_BINARY_DIR})
endif()

FetchContent_MakeAvailable( spdlog)

