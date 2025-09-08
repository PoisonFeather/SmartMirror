# Smart Mirror UI (PySide6) — Stratified Project

Minimalist, modern UI for a smart mirror. Python + PySide6.
Frameless fullscreen, auto-scaling typography, and modular widgets.

## Structure
smart_mirror/
app.py # Entry point
theme.py # Colors, font rules, base stylesheet
scale.py # DPI & screen-size scaling helpers
main_window.py # Main layout (grid) and window config
widgets/
init.py
clock.py # ClockWidget + GlowLabel
weather.py # WeatherWidget (placeholder for API)
agenda.py # AgendaWidget (placeholder for calendar)
services/
init.py
weather_service.py # TODO: Plug a weather API
calendar_service.py # TODO: Plug Google Calendar / ICS
requirements.txt
README.md
## Quick start
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m smart_mirror.app
Controls
Fullscreen by default; press Esc or Q to quit.

Notes
Design optimized for two-way mirrors: near-black background, high-contrast text, subtle glow.

Replace placeholder services with real data fetching.

yaml
Copy code

---

### `smart_mirror/__init__.py`
```python
# package marker