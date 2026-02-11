import QtQuick
import QtQuick.Controls
import SystemMonitor

ApplicationWindow {
    visible: true
    width: Screen.width > 800 ? 800 : Screen.width  // Responsive: Max 800 für Tablet, sonst Screen-Breite
    height: Screen.height > 1200 ? 1200 : Screen.height  // Max 1200 für Tablet
    title: "System Monitor"

    SystemInfo {
        id: systemInfo
    }

    Column {
        anchors.centerIn: parent
        spacing: Screen.height > 1000 ? 40 : 20  // Mehr Spacing für Tablet

        Text {
            text: "CPU: " + systemInfo.cpuUsage
            font.pixelSize: Screen.height > 1000 ? 32 : 24  // Größer für Tablet
            color: "blue"
        }

        Text {
            text: "RAM: " + systemInfo.ramUsage
            font.pixelSize: Screen.height > 1000 ? 32 : 24
            color: "green"
        }

        Text {
            text: "Storage: " + systemInfo.storageUsage
            font.pixelSize: Screen.height > 1000 ? 32 : 24
            color: "red"
        }
    }
}