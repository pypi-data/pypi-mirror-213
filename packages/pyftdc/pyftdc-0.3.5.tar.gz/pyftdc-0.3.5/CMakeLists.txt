cmake_minimum_required(VERSION 3.15)
project(pyftdc)

set(CMAKE_CXX_STANDARD 17)

message( "---------------------- library ${PROJECT_NAME} ----------------------------")

add_subdirectory(extern)
add_subdirectory(pybind11)
#add_subdirectory(Boost_tests)

pybind11_add_module(${PROJECT_NAME}
        src/python.cpp
        src/ConstDataRangeCursor.cpp
        src/Dataset.cpp
        src/FTDCParser.cpp
        src/MetricsToWTMap.cpp
        src/SampleLocation.cpp
        src/WriterTaskList.cpp
        src/ChunkMetric.cpp
        src/CSVWriter.cpp
        src/FileParsedData.cpp
        src/JSONWriter.cpp
        src/WriterTask.cpp
        src/ParserState.cpp
        src/BinaryBSON.cpp
        )

target_link_libraries(${PROJECT_NAME} PRIVATE bson_static)

target_include_directories(${PROJECT_NAME} PUBLIC
        ${CMAKE_BINARY_DIR}/_deps/spdlog-src/include
        ${CMAKE_SOURCE_DIR}/src/include

        )
target_link_libraries(${PROJECT_NAME}  PUBLIC
        ${CMAKE_DL_LIBS}
        bson_static
        z)

