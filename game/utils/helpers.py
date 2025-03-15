import random


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
