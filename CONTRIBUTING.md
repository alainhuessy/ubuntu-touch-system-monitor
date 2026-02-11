# Contributing

Vielen Dank für dein Interesse, zu diesem Projekt beizutragen! Wir freuen uns über Beiträge jeglicher Art.

## Wie du beitragen kannst

### Fehler melden (Issues)
- Verwende die GitHub-Issue-Vorlage für Bug-Reports.
- Beschreibe das Problem detailliert: Schritte zum Reproduzieren, erwartetes Verhalten, tatsächliches Verhalten.
- Füge Screenshots oder Logs hinzu, wenn möglich.

### Features vorschlagen
- Erstelle ein Issue mit der Bezeichnung "Feature Request".
- Beschreibe das gewünschte Feature und warum es nützlich wäre.

### Code beitragen
1. **Fork** das Repository.
2. **Clone** deinen Fork:
   ```bash
   git clone https://github.com/dein-username/ubuntu-touch-system-monitor.git
   cd ubuntu-touch-system-monitor
   ```
3. **Erstelle einen Branch** für deine Änderungen:
   ```bash
   git checkout -b feature/deine-feature
   ```
4. **Entwickle testgetrieben**:
   - Schreibe zuerst Tests (Qt Test für C++).
   - Implementiere die Funktionalität.
   - Stelle sicher, dass alle Tests grün sind.
5. **Committe deine Änderungen**:
   ```bash
   git add .
   git commit -m "Beschreibe deine Änderungen"
   ```
6. **Push** zu deinem Fork:
   ```bash
   git push origin feature/deine-feature
   ```
7. **Erstelle einen Pull Request** auf GitHub.

### Code-Standards
- **Testgetriebene Entwicklung (TDD):** Jede Funktion beginnt mit Tests.
- **C++17 und QML:** Halte dich an Qt-Best-Practices.
- **Dokumentation:** Füge Doxygen-Kommentare zu neuen Funktionen hinzu.
- **Commits:** Verwende klare, beschreibende Commit-Nachrichten.
- **Branches:** Verwende beschreibende Namen (z. B. `feature/cpu-optimization`, `fix/memory-leak`).

### Testen
- Führe alle Tests aus: `cd build && make test_systeminfo && ./test_systeminfo`
- Teste auf Ubuntu Touch-Geräten (Volla-Tablet/Phone), wenn möglich.
- Stelle sicher, dass der Build erfolgreich ist: `clickable build`

### Lizenz
Durch das Beitragen stimmst du zu, dass deine Beiträge unter der MIT-Lizenz veröffentlicht werden.

## Kontakt
Bei Fragen: Öffne ein Issue oder kontaktiere Alain Huessy (alain@example.com).