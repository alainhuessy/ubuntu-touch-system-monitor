file(REMOVE_RECURSE
  "SystemMonitor/qml/Main.qml"
)

# Per-language clean rules from dependency scanning.
foreach(lang )
  include(CMakeFiles/systemmonitor_tooling.dir/cmake_clean_${lang}.cmake OPTIONAL)
endforeach()
