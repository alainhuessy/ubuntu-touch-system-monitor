# GitHub Copilot – Arbeitsanweisung

Du arbeitest **testgetrieben**.

## Regeln
- Schreibe zuerst Tests (Qt Test für C++)
- Keine Implementierung ohne Test
- Halte Funktionen klein
- Erkläre jede Funktion auf Deutsch
- Nutze Qt/C++ Best Practices

## Ziel
Eine native Ubuntu Touch Systemmonitor App mit QML und C++, optimiert für Volla-Tablet und OpenStore.

- [x] Verify that the copilot-instructions.md file in the .github directory is created.

- [x] Clarify Project Requirements
	<!-- Ubuntu Touch Systemmonitor App mit QML und C++, für Volla-Tablet, Ubuntu Touch Store. -->

- [x] Scaffold the Project
	<!-- Grundlegende Struktur erstellt: CMakeLists.txt, main.cpp, Main.qml, manifest.json, clickable.json. -->

- [ ] Customize the Project
	<!-- Implementiere Systemmonitor-Funktionen (CPU, RAM, Speicher). -->

- [ ] Install Required Extensions
	<!-- Keine spezifischen Extensions benötigt. -->

- [ ] Compile the Project
	<!-- Installiere Clickable, baue mit CMake. -->

- [ ] Create and Run Task
	<!-- Erstelle Task für Clickable build. -->

- [ ] Launch the Project
	<!-- Teste auf Ubuntu Touch Device. -->

- [x] Ensure Documentation is Complete
	<!-- README.md und copilot-instructions.md aktualisieren. -->

- [ ] Phase 6: Batteriestatus hinzufügen
	<!-- Batterie-Level, Ladezustand und Restlaufzeit implementieren. Tests zuerst, dann C++/QML, Apparmor aktualisieren. -->

- [ ] Phase 7: Temperaturüberwachung hinzufügen
	<!-- CPU-Temperatur mit Warnfarben anzeigen. Tests, C++, QML, Apparmor. -->

- [ ] Phase 8: Netzwerk-Statistiken hinzufügen
	<!-- Upload/Download-Raten anzeigen. Tests, C++, QML, Apparmor. -->

- [ ] Phase 9: Prozessliste hinzufügen
	<!-- Top-Prozesse nach CPU/RAM. Tests, C++, QML, Apparmor. -->

- [ ] Phase 10: Historische Daten und Diagramme hinzufügen
	<!-- Trends mit Charts. Tests, C++, QML, QtCharts hinzufügen. -->

- [ ] Phase 11: Benachrichtigungen hinzufügen
	<!-- Alarme bei hohen Auslastungen. Tests, C++, QML, Notification API. -->
