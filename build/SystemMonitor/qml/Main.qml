import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import SystemMonitor

ApplicationWindow {
    visible: true
    width: Screen.width > 800 ? 800 : Screen.width
    height: Screen.height > 1200 ? 1200 : Screen.height
    title: "System Monitor"

    SystemInfo {
        id: systemInfo
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 20

        Text {
            text: "System Monitor"
            font.pixelSize: Screen.height > 1000 ? 36 : 28
            Layout.alignment: Qt.AlignHCenter
            color: "black"
        }

        // CPU Section
        RowLayout {
            Layout.fillWidth: true
            spacing: 10

            Text {
                text: "CPU"
                font.pixelSize: Screen.height > 1000 ? 24 : 18
                Layout.preferredWidth: 60
            }

            ProgressBar {
                value: parseFloat(systemInfo.cpuUsage) / 100.0
                Layout.fillWidth: true
                from: 0
                to: 1
            }

            Text {
                text: systemInfo.cpuUsage
                font.pixelSize: Screen.height > 1000 ? 24 : 18
                Layout.preferredWidth: 80
            }
        }

        // RAM Section
        RowLayout {
            Layout.fillWidth: true
            spacing: 10

            Text {
                text: "RAM"
                font.pixelSize: Screen.height > 1000 ? 24 : 18
                Layout.preferredWidth: 60
            }

            ProgressBar {
                value: calculateRamUsage()
                Layout.fillWidth: true
                from: 0
                to: 1
            }

            Text {
                text: systemInfo.ramUsage
                font.pixelSize: Screen.height > 1000 ? 24 : 18
                Layout.preferredWidth: 150
            }
        }

        // Storage Section
        RowLayout {
            Layout.fillWidth: true
            spacing: 10

            Text {
                text: "Storage"
                font.pixelSize: Screen.height > 1000 ? 24 : 18
                Layout.preferredWidth: 60
            }

            ProgressBar {
                value: calculateStorageUsage()
                Layout.fillWidth: true
                from: 0
                to: 1
            }

            Text {
                text: systemInfo.storageUsage
                font.pixelSize: Screen.height > 1000 ? 24 : 18
                Layout.preferredWidth: 150
            }
        }

        Item {
            Layout.fillHeight: true
        }
    }

    function calculateRamUsage() {
        var parts = systemInfo.ramUsage.split(" / ");
        if (parts.length === 2) {
            var used = parseInt(parts[0].split(" ")[0]);
            var total = parseInt(parts[1].split(" ")[0]);
            return used / total;
        }
        return 0;
    }

    function calculateStorageUsage() {
        var parts = systemInfo.storageUsage.split(" / ");
        if (parts.length === 2) {
            var used = parseInt(parts[0].split(" ")[0]);
            var total = parseInt(parts[1].split(" ")[0]);
            return used / total;
        }
        return 0;
    }
}