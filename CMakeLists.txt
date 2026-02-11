cmake_minimum_required(VERSION 3.16)
project(systemmonitor)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Core Quick Test)

qt_standard_project_setup()

qt_add_executable(systemmonitor
    src/main.cpp
    src/systeminfo.cpp
)

qt_add_qml_module(systemmonitor
    URI SystemMonitor
    VERSION 1.0
    QML_FILES qml/Main.qml
)

target_link_libraries(systemmonitor
    PRIVATE Qt6::Core Qt6::Quick
)

# Tests
qt_add_executable(test_systeminfo
    tests/test_systeminfo.cpp
    tests/test_systeminfo.h
    src/systeminfo.cpp
)

target_link_libraries(test_systeminfo
    PRIVATE Qt6::Core Qt6::Test
)

target_include_directories(test_systeminfo PRIVATE src tests)

install(TARGETS systemmonitor
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)