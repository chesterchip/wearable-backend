from datetime import datetime, timedelta

# Raw timeline entries with relative hour offsets and descriptions
events_timeline = [
    {"hour_offset": -24, "type": "meal",     "desc": "Breakfast"},
    {"hour_offset": -20, "type": "exercise", "desc": "Morning Run"},
    {"hour_offset": -18, "type": "coffee",   "desc": "Coffee"},
    {"hour_offset": -12, "type": "meal",     "desc": "Lunch"},
    {"hour_offset": -8,  "type": "exercise", "desc": "Afternoon Gym"},
    {"hour_offset": -6,  "type": "caffeine", "desc": "Afternoon Coffee"},
    {"hour_offset": -4,  "type": "meal",     "desc": "Dinner"},
    {"hour_offset": -2,  "type": "sleep",    "desc": "Night Sleep"},
]

# Recommended durations per event type
_EVENT_DURATIONS = {
    "meal":     timedelta(hours=1, minutes=30),
    "exercise": timedelta(hours=1),
    "coffee":   timedelta(minutes=30),
    "caffeine": timedelta(minutes=30),
    "sleep":    timedelta(hours=8),
}

# Color mapping by description
_COLOR_MAP = {
    "Breakfast":      "#ffcc80",
    "Morning Run":    "#ff9800",
    "Coffee":         "#bcaaa4",
    "Lunch":          "#a5d6a7",
    "Afternoon Gym":  "#4caf50",
    "Afternoon Coffee":"#9fa8da",
    "Dinner":         "#795548",
    "Night Sleep":    "#9fa8da",
}

def build_event_list():
    """
    Convert events_timeline entries into absolute start/end
    timestamps (ms since epoch), with category, desc, and color.
    """
    now = datetime.utcnow()
    out = []
    for e in events_timeline:
        start = now + timedelta(hours=e["hour_offset"])
        duration = _EVENT_DURATIONS.get(e["type"], timedelta(hours=1))
        end = start + duration

        out.append({
            "start":    int(start.timestamp() * 1000),
            "end":      int(end.timestamp()   * 1000),
            "category": e["desc"],
            "desc":     e["desc"],
            "color":    _COLOR_MAP.get(e["desc"], "#90a4ae"),
        })
    return out
