# GitHub Copilot – Implementierungsspezifikation
# Projekt: Bauwerksdokumentations-Prüfer (12er / KBOB)

---

## 🎯 Projektziel (verbindlich)

Implementiere ein **lokal lauffähiges Python-Tool**, das Bauwerksdokumentationen
nach **zwei unterschiedlichen Strukturstandards** prüft:

- 12er-Struktur (vereinfachte, klassische Ablagestruktur)
- KBOB-Struktur (Schweizer Branchenstandard)

Das Tool prüft **Struktur, Dateinamen, Inhalte und Konsistenz** und erzeugt
einen **HTML-Prüfbericht**.  
Alle Prüfungen laufen **ausschließlich lokal**, **offline**, **ohne Admin-Rechte**
und **ohne Cloud-Dienste**.

---

## 🧠 Grundprinzipien (NICHT VERHANDELBAR)

### 1. Testgetriebene Entwicklung (TDD)
- **Jede Funktion beginnt mit pytest-Tests**
- Tests müssen zuerst **fehlschlagen**
- Erst danach Implementierung
- Erst wenn **alle Tests grün** sind → nächster Schritt

### 2. Code-Qualität
- Python **3.11**
- **PEP8-konform**
- Kleine, gut testbare Funktionen
- Keine globalen Seiteneffekte
- Klare Modultrennung

### 3. Dokumentation
- Jede Funktion besitzt:
  - Deutschen Docstring
  - Typannotationen
  - Klare Beschreibung der Seiteneffekte

### 4. Pfadsicherheit
- Ausschließlich `pathlib`
- Keine Arbeit außerhalb erlaubter Projektpfade
- **Pfad-Ausbruch ist verboten**

### 5. Plattformunabhängigkeit
- Windows & macOS
- Keine Annahmen über `/` oder `\`
- Keine hardcodierten Pfade

---

## 🚫 Verbotene Dinge

Copilot DARF NICHT:
- virtuelle Umgebungen (.venv) anlegen
- Adminrechte voraussetzen
- Internetzugriffe durchführen
- externe APIs verwenden
- Dateien ohne Bestätigung verändern
- Logik in die GUI verschieben
- Tests überspringen

---

## 🧩 Fachliche Rahmenbedingungen

### Projektinput
- Ein oder mehrere Projektordner
- Projektordner liegen auf Netzwerklaufwerken
- Nur Pfade aus `.env` / `settings.yaml` sind erlaubt

### Strukturdefinition
- Wird **bei jeder Prüfung neu** aus einer Excel-Datei geladen
- Struktur ist **dynamisch**
- Anzahl Ebenen kann variieren
- Einträge können:
  - Verzeichnisse
  - Pflichtdokumente
  - optionale Dokumente sein

---

## 🔁 Gesamtprogrammablauf (fachlich)

0. Struktur (12er oder KBOB) auswählen und Excel laden  
1. Projekt-Backup erstellen  
2. Projektordner vollständig scannen (rekursiv)  
3. macOS-Dateien erkennen und optional löschen  
4. Dateinamen normalisieren (Umlaute, Kodierungsfehler)  
5. Ordnerstruktur prüfen und ggf. korrigieren  
6. Dateinummern prüfen, verschieben, ergänzen  
7. Erste Inhaltsprüfung (leer / Platzhalter / Planerkennung)  
8. HTML-Prüfbericht erzeugen  
9. Ergebnisse in GUI anzeigen  

---

## 📐 Entwicklungsphasen (zwingende Reihenfolge)

---

### 🔹 PHASE 1 – Projektgrundlage & Infrastruktur

**Ziel:** lauffähiges Grundgerüst mit Tests

Aufgaben:
- Projektstruktur gemäß `STRUKTUR.md` anlegen
- Logging-Grundlage erstellen
- Konfigurationsladefunktion implementieren

Tests:
- Projekt kann importiert werden
- Logging erzeugt Logdatei
- Konfiguration wird korrekt geladen

Ergebnis:
- Basis steht
- Keine Fachlogik

---

### 🔹 PHASE 2 – Excel-Strukturimport

**Ziel:** Strukturdefinition aus Excel robust einlesen

Aufgaben:
- Excel-Datei laden
- Relevante Spalten erkennen
- Interne Strukturrepräsentation erzeugen

Tests:
- Excel mit variabler Tiefe
- Ungültige Zeilen
- Leere Excel
- Unterschiedliche Strukturstandards

Ergebnis:
- Struktur als Python-Objekt verfügbar
- Keine Abhängigkeit von GUI

---

### 🔹 PHASE 3 – Projekt-Scan & Sicherheit

**Ziel:** Projektordner vollständig und sicher erfassen

Aufgaben:
- Rekursiver Scan aller Dateien & Ordner
- Pfadvalidierung gegen erlaubte Root-Pfade
- Metadaten erfassen

Tests:
- Erlaubter Pfad → OK
- Nicht erlaubter Pfad → Abbruch
- Symlink-Ausbruch verhindern

Ergebnis:
- Vollständige Ist-Struktur

---

### 🔹 PHASE 4 – Ordnerstrukturprüfung

**Ziel:** Soll- vs. Ist-Struktur vergleichen

Aufgaben:
- Fehlende Ordner erkennen
- Zusätzliche Ordner erkennen
- Falsche Ebene erkennen
- Vorschläge zur Korrektur erzeugen

Tests:
- Fehlende Hauptordner
- Fehlende Unterordner
- Doppelte Ordner
- Inkonsistente Nummerierung

Ergebnis:
- Struktur-Diff als Datenobjekt

---

### 🔹 PHASE 5 – Dateinamen- & Nummernlogik

**Ziel:** Einheitliche Dateibenennung sicherstellen

Aufgaben:
- Umlaute & Kodierungsfehler korrigieren
- Dateinummern prüfen
- Dateien ggf. verschieben
- Nummern fortlaufend vergeben

Tests:
- Umlautersetzung
- Nummer doppelt
- Nummer fehlt
- Datei im falschen Ordner

Ergebnis:
- Umbenennungsvorschläge
- Keine automatische Änderung ohne Bestätigung

---

### 🔹 PHASE 6 – Inhaltsbasierte Basisprüfung

**Ziel:** offensichtliche Inhaltsprobleme erkennen

Aufgaben:
- Leere Dateien erkennen
- Platzhaltertexte erkennen
- Pläne klassifizieren

Tests:
- 0-Byte-Datei
- Platzhaltertext
- PDF ohne Text
- Planformate (DWG, PDF-Plan)

Ergebnis:
- Markierte Dateien im Bericht

---

### 🔹 PHASE 7 – HTML-Prüfbericht

**Ziel:** nachvollziehbarer, professioneller Bericht

Aufgaben:
- HTML-Template verwenden
- Tabellen & Diagramme erzeugen
- Hyperlinks zu Dateien
- Zusammenfassung
- **Korrekte hierarchische Darstellung:** Baumstruktur mit depth-basierter Einrückung für beide Strukturtypen (12er und KBOB)

Tests:
- Bericht wird erzeugt
- Enthält alle Pflichtsektionen
- Links korrekt
- Hierarchie korrekt eingerückt

Ergebnis:
- HTML-Bericht im Projektordner

---

### 🔹 PHASE 8 – Streamlit-GUI

**Ziel:** Benutzerfreundliche Oberfläche mit Datenintegration

Aufgaben:
- Projekt- & Strukturauswahl
- **JSON-basierte Datenintegration:**
  - Lädt Vergleichsergebnisse aus `structure_analysis_result.json`
  - Zeigt SOLL-IST-Vergleich visuell an
  - Interaktive Baumstruktur mit Status-Farbcodes
  - Filterbare Listen (fehlend/zusätzlich korrekt/falsch)
- Fortschrittsanzeige
- Echtzeit-Vorschau
- Expertenmodus (ausklappbar)

Architektur:
- **Datenquelle:** JSON-Dateien aus Phase 4-7
- **Präsentation:** Reine Anzeigelogik, keine Vergleichslogik
- **Interaktivität:** Filter, Suche, Export-Optionen

Tests:
- Smoke-Test (App startet)
- JSON-Ladevorgang
- GUI-Interaktionen
- Konfigurationswechsel

Ergebnis:
- GUI als Einstiegspunkt mit voller Datenintegration

---

## 🏗️ Architekturprinzipien

### Datenfluss-Architektur
- **Phase 4-7:** Vergleichslogik → JSON-Output (`structure_analysis_result.json`)
- **Phase 8:** GUI lädt JSON → Interaktive Visualisierung
- **Trennung:** Logik (Phasen 1-7) ↔ Präsentation (Phase 8)

### JSON-Struktur Standard
Alle Analyseergebnisse folgen einheitlichem JSON-Format:
```json
{
  "metadata": {"timestamp": "...", "sources": {...}},
  "summary": {"fehlend": 0, "zusätzlich_korrekt": 0, "zusätzlich_falsch": 0},
  "details": {"fehlend": [...], "zusätzlich_korrekt": [...], "zusätzlich_falsch": [...]},
  "tree_structure": {...}
}
```

### Wiederverwendbarkeit
- JSON-Daten können von HTML-Berichten, GUI und zukünftigen APIs genutzt werden
- Klare Trennung von Berechnung und Darstellung
- Offline-fähig und cachbar

---

## 🧪 Tests – verbindliche Regeln

- Tests liegen ausschließlich in `tests/`
- Testdaten ausschließlich in `tests/data/`
- Keine echten Projektdaten
- Tests müssen reproduzierbar sein

---

## 🔐 Sicherheitsregeln

- Keine Dateimanipulation ohne Bestätigung
- Backup vor jeder Änderung
- Keine Daten außerhalb Projektordner
- Logging aller Änderungen

---

## 📌 Definition of Done (DoD)

Ein Feature gilt als abgeschlossen, wenn:
- Alle Tests grün sind
- Code dokumentiert ist
- Keine Pfadunsicherheiten existieren
- Keine Seiteneffekte ohne Logging auftreten
- Feature plattformunabhängig funktioniert

---

## 🧠 Erweiterungen (NICHT JETZT)

- LLM / NER / Embeddings
- FAISS / SQLite
- llama-cpp-python (GGUF)

Diese Themen sind **explizit außerhalb der Basisimplementierung**
und werden erst nach stabiler Kernfunktion betrachtet.
