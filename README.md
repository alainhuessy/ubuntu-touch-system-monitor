# Ubuntu Touch System Monitor

Eine native Systemmonitor-App für Ubuntu Touch, optimiert für Volla-Tablet (8") und Volla-Phone (6.3"). Zeigt Echtzeit-Informationen zu CPU-Auslastung, RAM-Verbrauch und Speicherplatz an.

## Features

- **Echtzeit-Updates:** Automatische Aktualisierung alle 2 Sekunden
- **Responsive UI:** Optimiert für verschiedene Bildschirmgrößen (Volla-Fokus)
- **Touch-optimiert:** Einfache Bedienung auf mobilen Geräten
- **Sicher:** Keine Root-Zugriffe, respektiert Ubuntu Touch Berechtigungen

## Screenshots

*(Füge hier Screenshots der App hinzu)*

## Installation

### Aus dem OpenStore (empfohlen)
1. Öffne den OpenStore auf deinem Ubuntu Touch-Gerät
2. Suche nach "System Monitor"
3. Installiere die App

### Manuell aus Source
1. Klone das Repository:
   ```bash
   git clone https://github.com/alainhuessy/ubuntu-touch-system-monitor.git
   cd ubuntu-touch-system-monitor
   ```

2. Installiere Abhängigkeiten:
   ```bash
   sudo apt install qt6-base-dev qt6-declarative-dev cmake
   snap install clickable --classic
   ```

3. Baue das Click-Package:
   ```bash
   clickable build
   clickable install
   ```

## Entwicklung

### Voraussetzungen
- Ubuntu 20.04 oder neuer
- Qt6, CMake, Clickable

### Build
```bash
mkdir build && cd build
cmake ..
make
./systemmonitor  # Test auf Desktop
```

### Tests
```bash
cd build
make test_systeminfo
./test_systeminfo
```

## Architektur

- **QML:** Benutzeroberfläche (responsive, touch-optimiert)
- **C++:** Backend-Logik (Systemdaten aus /proc, Qt Signals/Slots)
- **CMake:** Build-System
- **Clickable:** Ubuntu Touch Packaging

## Beitragen

1. Fork das Repository
2. Erstelle einen Feature-Branch
3. Committe deine Änderungen
4. Erstelle einen Pull Request

## Lizenz

MIT License - siehe [LICENSE](LICENSE) für Details.

## Kontakt

Alain Huessy - alainhuessy@gmx.ch

Projekt-Link: [https://github.com/alainhuessy/ubuntu-touch-system-monitor](https://github.com/alainhuessy/ubuntu-touch-system-monitor)