cmake_minimum_required(VERSION 3.16)
project(systemmonitor)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Core Quick)

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

install(TARGETS systemmonitor
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)