#!/usr/bin/env python3
"""
Haupt-Einstiegspunkt für das Bauwerksdokumentations-Prüfer Paket.

Dieses Modul ermöglicht die Ausführung des Projekts als Python-Modul:
python -m src

Es bietet ein einfaches CLI-Menü für die verfügbaren Funktionen.
"""

import sys
from pathlib import Path
import logging

# Pfad zum Projekt hinzufügen
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.logging_config import setup_logging


def show_menu():
    """Zeigt das Hauptmenü an."""
    print("🏗️  Bauwerksdokumentations-Prüfer")
    print("=" * 40)
    print("Verfügbare Funktionen:")
    print("1. Beispiel-Scan (Dateiliste mit Metadaten)")
    print("2. Schnellanalyse (erste Ebene)")
    print("3. Schnelltest (nur Ordnerstruktur)")
    print("4. Struktur validieren")
    print("5. READMEs aktualisieren")
    print("6. Struktur visualisieren")
    print("0. Beenden")
    print()


def run_example_scan():
    """Führt example_scan.py aus."""
    print("Starte Beispiel-Scan...")
    try:
        from scripts.example_scan import main
        main()
    except Exception as e:
        logging.error(f"Fehler beim Beispiel-Scan: {e}")
        print(f"Fehler: {e}")


def run_fast_analysis():
    """Führt fast_analysis.py aus."""
    print("Starte Schnellanalyse...")
    try:
        from scripts.fast_analysis import main
        main()
    except Exception as e:
        logging.error(f"Fehler bei Schnellanalyse: {e}")
        print(f"Fehler: {e}")


def run_quick_scan():
    """Führt quick_scan.py aus."""
    print("Starte Schnelltest...")
    try:
        from scripts.quick_scan import main
        main()
    except Exception as e:
        logging.error(f"Fehler beim Schnelltest: {e}")
        print(f"Fehler: {e}")


def run_validate_structure():
    """Führt validate_structure.py aus."""
    print("Starte Strukturvalidierung...")
    try:
        from scripts.validate_structure import main
        main()
    except Exception as e:
        logging.error(f"Fehler bei Strukturvalidierung: {e}")
        print(f"Fehler: {e}")


def run_update_readmes():
    """Führt update_readmes.py aus."""
    print("Starte README-Aktualisierung...")
    try:
        from scripts.update_readmes import main
        main()
    except Exception as e:
        logging.error(f"Fehler bei README-Aktualisierung: {e}")
        print(f"Fehler: {e}")


def run_visualize_structure():
    """Führt visualize_structure.py aus."""
    print("Starte Strukturvisualisierung...")
    try:
        from src.visualize_structure import main
        main()
    except Exception as e:
        logging.error(f"Fehler bei Strukturvisualisierung: {e}")
        print(f"Fehler: {e}")


def main():
    """Hauptfunktion für das CLI-Menü."""
    # Logging einrichten
    log_file = project_root / "scripts_log.txt"
    setup_logging(log_file)
    logging.info("Starte Bauwerksdokumentations-Prüfer als Modul")

    # Prüfe Kommandozeilenargumente oder piped input
    if len(sys.argv) > 1:
        # Nicht-interaktiver Modus: Argument als Wahl verwenden
        choice = sys.argv[1].strip()
        logging.info(f"Nicht-interaktiver Modus mit Wahl: {choice}")
    elif not sys.stdin.isatty():
        # Piped input Modus
        choice = sys.stdin.read().strip()
        logging.info(f"Piped input Modus mit Wahl: {choice}")
    else:
        # Interaktiver Modus
        print("🏗️  Bauwerksdokumentations-Prüfer - Modul-Modus")
        print("Willkommen! Wählen Sie eine Funktion aus dem Menü.")
        print()
        show_menu()
        try:
            choice = input("Ihre Wahl (0-6): ").strip()
        except EOFError:
            # Bei piped input oder fehlender Eingabe
            print("Keine Eingabe erhalten. Verwenden Sie: python -m src <zahl>")
            logging.info("Beende wegen fehlender Eingabe")
            return

    # Wahl verarbeiten (vereinfacht - keine Schleife mehr)
    try:
        if choice == "0":
            print("Auf Wiedersehen!")
            logging.info("Beende Bauwerksdokumentations-Prüfer")
        elif choice == "1":
            run_example_scan()
        elif choice == "2":
            run_fast_analysis()
        elif choice == "3":
            run_quick_scan()
        elif choice == "4":
            run_validate_structure()
        elif choice == "5":
            run_update_readmes()
        elif choice == "6":
            run_visualize_structure()
        else:
            print("❌ Ungültige Wahl. Bitte 0-6 eingeben.")
            logging.warning(f"Ungültige Wahl: {choice}")
            if len(sys.argv) == 1:  # Nur im interaktiven Modus
                print("Drücken Sie Enter zum Fortfahren...")
                input()

    except KeyboardInterrupt:
        print("\n\nAuf Wiedersehen! (Strg+C)")
        logging.info("Beende Bauwerksdokumentations-Prüfer (KeyboardInterrupt)")
    except Exception as e:
        logging.error(f"Unerwarteter Fehler: {e}")
        print(f"❌ Fehler: {e}")


if __name__ == "__main__":
    main()