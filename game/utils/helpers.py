import random
import json


def load_json(cls):
    """
    Ładuje dane z pliku JSON i tworzy instancje klasy.

    Args:
        cls: Klasa, której instancje mają być tworzone.

    Returns:
        Lista instancji klasy.
    """
    file_name = cls.__name__.lower()
    file_path = f"data/{file_name}s.json"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            instances = [instance for instance in data]
            return instances
    except FileNotFoundError:
        print(f"Błąd: Plik {file_path} nie został znaleziony.")
        return []
    except json.JSONDecodeError:
        print(f"Błąd: Plik {file_path} zawiera niepoprawne dane JSON.")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd podczas ładowania danych z pliku "
              f"{file_path}: {e}")
    return []


def generate_random_number(min_value, max_value):
    """Generuje losową liczbę całkowitą z podanego zakresu."""
    return random.randint(min_value, max_value)


def format_text(text, width=80):
    """Formatuje tekst, aby mieścił się w określonej szerokości."""
    lines = []
    words = text.split()
    current_line = ""
    for word in words:
        if len(current_line + word) + 1 <= width:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())
    return "\n".join(lines)
