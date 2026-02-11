from pathlib import Path


def is_path_allowed(target_path: Path, allowed_roots: list[Path]) -> bool:
    """
    Prüft, ob sich ein Zielpfad innerhalb eines der erlaubten Root-Pfade befindet.

    Diese Funktion verhindert, dass das Programm außerhalb der definierten
    Projektverzeichnisse arbeitet (z. B. via ../../).

    :param target_path: Zu prüfender Pfad
    :param allowed_roots: Liste erlaubter Root-Pfade
    :return: True, wenn erlaubt, sonst False
    """
    try:
        target_path = target_path.resolve()
        for root in allowed_roots:
            if target_path.is_relative_to(root.resolve()):
                return True
        return False
    except Exception:
        return False


def is_allowed_subfolder(path: Path, structure: list[dict]) -> bool:
    """
    Prüft, ob ein Pfad ein erlaubter Unterordner gemäß der Dokumentationsregel ist.

    Erlaubte Unterordner sind Fortsetzungen bestehender Nummern (z.B. 11.06101 unter 11.061).

    :param path: Zu prüfender Pfad
    :param structure: Strukturdefinition als Liste von Dicts
    :return: True, wenn erlaubt, sonst False
    """
    parts = path.parts
    # Finde die letzte bekannte Nummer im Pfad
    for i in range(len(parts) - 1, -1, -1):
        potential_number = parts[i]
        if any(item['number'] == potential_number for item in structure):
            # Prüfe, ob der nächste Teil eine Fortsetzung ist
            if i + 1 < len(parts):
                next_part = parts[i + 1]
                if next_part.startswith(potential_number) and len(next_part) > len(potential_number):
                    return True
    return False
