# GitHub Copilot – Implementierungsspezifikation
# Projekt: Ubuntu Touch System Monitor für Volla-Geräte

---

## 📋 Gesamtplan (TL;DR)
Entwickle eine native Ubuntu Touch App zur Echtzeit-Anzeige von CPU, RAM und Speicher, optimiert für Volla-Tablet (8") und Volla-Phone (6.3"), aber kompatibel mit allen Ubuntu Touch-Geräten durch responsive QML-Layouts. Testgetriebene Entwicklung mit Qt/C++, von Grundstruktur bis OpenStore-Submission. Fokus auf Sicherheit, Performance und Touch-Optimierung.

### Schritte (Steps)
1. **PHASE 1: Projektgrundlage** – Erstelle CMake-Struktur, Basis-QML UI mit responsive Elementen für Volla-Bildschirmgrößen, C++ SystemInfo-Klasse (Platzhalter). Tests: Kompilierung und UI-Ladung auf simulierten Größen.
2. **PHASE 2: Systeminformationen** – Implementiere echte Datenabfrage aus /proc/stat, /proc/meminfo, df. Qt Signals für Updates. Tests: Datenkorrektheit und Signal-Emission.
3. **PHASE 3: UI-Polish** – Responsive QML-Layouts (z. B. kompakt für 6.3", erweitert für 8"), Touch-Gesten, Icons. Tests: UI auf verschiedenen Geräten.
4. **PHASE 4: Packaging** – Click-Package mit Manifest.json, Apparmor-Profil, Desktop-Datei. Clickable Build testen. Tests: Package-Installation auf Ubuntu Touch.
5. **PHASE 5: Store-Submission** – Finale Tests auf Volla- und anderen Geräten, Dokumentation (README, Screenshots). OpenStore-Upload vorbereiten.

### Verifikation (Verification)
- **Tests:** Qt Test für C++, QML-Tests optional; alle Phasen mit grünen Tests abschließen.
- **Build:** CMake erfolgreich, Clickable-Package erstellbar.
- **Laufzeit:** App startet auf Ubuntu Touch-Emulator und realen Geräten (Volla-Fokus).
- **Kompatibilität:** Keine Fehler auf anderen Ubuntu Touch-Geräten.

### Entscheidungen (Decisions)
- **Volla-Fokus:** Spezifische Optimierungen (z. B. Layouts), aber allgemeine Kompatibilität durch responsive Design.
- **Technologie:** QML + C++ für native Performance, keine Python-Alternativen.

---

## 🎯 Projektziel (verbindlich)

Implementiere eine **native Ubuntu Touch App**, die Systeminformationen (CPU, RAM, Speicher) in Echtzeit anzeigt. Die App läuft auf Ubuntu Touch-Geräten wie dem Volla-Tablet und ist für den OpenStore optimiert.

- **Technologie:** QML für UI, C++ für Logik, CMake für Build.
- **Plattform:** Ubuntu Touch (ARM-basiert).
- **Vertrieb:** OpenStore (kostenlos, Open-Source).

---

## 🧠 Grundprinzipien (NICHT VERHANDELBAR)

### 1. Testgetriebene Entwicklung (TDD)
- **Jede Funktion beginnt mit Tests** (Qt Test für C++).
- Tests müssen zuerst **fehlschlagen**.
- Erst danach Implementierung.
- Erst wenn **alle Tests grün** sind → nächster Schritt.

### 2. Code-Qualität
- C++17, QML-konform.
- Klare Trennung: UI (QML) ↔ Logik (C++).
- Keine globalen Seiteneffekte.
- Modularer Aufbau.

### 3. Dokumentation
- Jede Funktion/C++-Klasse besitzt:
  - Doxygen-Kommentare.
  - Klare Beschreibung der Seiteneffekte.

### 4. Sicherheit
- Keine unsicheren Systemaufrufe.
- Respektiere Ubuntu Touch Berechtigungen.

### 5. Plattformunabhängigkeit
- Optimiert für ARM/Ubuntu Touch.
- Keine Annahmen über Hardware.

---

## 🚫 Verbotene Dinge

Copilot DARF NICHT:
- Nicht-Qt Frameworks verwenden.
- Internetzugriffe ohne Berechtigung.
- Unsichere Code-Praktiken.
- Tests überspringen.

---

## 🧩 Fachliche Rahmenbedingungen

### App-Funktionen
- Echtzeit-Anzeige von CPU-Auslastung, RAM-Verbrauch, Speicherplatz.
- Einfache, touch-optimierte UI.
- Hintergrund-Updates alle 1-2 Sekunden.

### Technische Anforderungen
- Click-Package für OpenStore.
- Manifest.json mit korrekten Metadaten.
- Apparmor-Profil für Systemzugriffe.

---

## 🔁 Gesamtprogrammablauf (fachlich)

1. App starten und UI laden.
2. Systeminformationen sammeln (C++ Backend).
3. Daten an QML UI senden.
4. UI aktualisieren und anzeigen.
5. Bei App-Schließen Ressourcen freigeben.

---

## 📐 Entwicklungsphasen (zwingende Reihenfolge)

### 🔹 PHASE 1 – Projektgrundlage
**Ziel:** Grundstruktur mit CMake, QML, C++.

Aufgaben:
- CMakeLists.txt für Qt/QML.
- Basis-QML UI.
- Einfache C++-Klasse für Systeminfo (Platzhalter).

Tests:
- App kompiliert.
- UI lädt.

### 🔹 PHASE 2 – Systeminformationen
**Ziel:** Echte Systemdaten sammeln.

Aufgaben:
- C++-Code für CPU/RAM/Speicher lesen.
- Qt Signals für UI-Updates.

Tests:
- Daten werden korrekt gelesen.
- Updates funktionieren.

### 🔹 PHASE 3 – UI-Polish
**Ziel:** Touch-optimierte UI.

Aufgaben:
- Responsive Design.
- Icons und Farben.

### 🔹 PHASE 4 – Packaging
**Ziel:** Click-Package erstellen.

Aufgaben:
- Manifest.json, Apparmor, Desktop-Datei.
- Clickable Build testen.

### 🔹 PHASE 5 – Store-Submission
**Ziel:** Für OpenStore vorbereiten.

Aufgaben:
- Finale Tests.
- Dokumentation.

---

## 🏗️ Architekturprinzipien

- **MVC:** QML (View), C++ (Model/Controller).
- **Signals/Slots:** Für Datenfluss.
- **Modular:** Trennung von UI und Logik.

---

## 🧪 Tests – verbindliche Regeln

- Qt Test für C++.
- QML-Tests optional.

---

## 🔐 Sicherheitsregeln

- Nur notwendige Berechtigungen.
- Keine Root-Zugriffe.

---

## 📌 Definition of Done (DoD)

Ein Feature gilt als abgeschlossen, wenn:
- Alle Tests grün sind.
- Code dokumentiert ist.
- App auf Ubuntu Touch läuft.
- Click-Package erstellbar ist.
