import QtQuick
import QtQuick.Controls
import SystemMonitor

ApplicationWindow {
    visible: true
    width: 400
    height: 600
    title: "System Monitor"

    SystemInfo {
        id: systemInfo
    }

    Column {
        anchors.centerIn: parent
        spacing: 20

        Text {
            text: "CPU: " + systemInfo.cpuUsage
            font.pixelSize: 24
        }

        Text {
            text: "RAM: " + systemInfo.ramUsage
            font.pixelSize: 24
        }

        Text {
            text: "Storage: " + systemInfo.storageUsage
            font.pixelSize: 24
        }
    }
}