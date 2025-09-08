# Placeholder calendar service; integrate Google Calendar or read ICS.
# Provide a function like get_today_events() -> list[tuple[str, str]]

from datetime import datetime

def get_today_events() -> list[tuple[str, str]]:
    # TODO: replace with actual calendar entries
    # Return a list of (time_str, text) tuples.
    return [
        ("08:30", "Standup proiect"),
        ("12:00", "Prânz cu Alex"),
        ("16:30", "Gym · Pull day"),
    ]
