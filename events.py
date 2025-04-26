# events.py
from datetime import datetime, timedelta

now = datetime.utcnow()
# relative offsets for demo
events = [
    {
      "desc": "Breakfast",
      "category": "Eating & Drinking",
      "color": "#4caf50",
      "start": (now - timedelta(hours=22)).isoformat()+"Z",
      "end":   (now - timedelta(hours=21, minutes=30)).isoformat()+"Z",
    },
    {
      "desc": "Morning Run",
      "category": "Exercise",
      "color": "#ff9800",
      "start": (now - timedelta(hours=18)).isoformat()+"Z",
      "end":   (now - timedelta(hours=17, minutes=30)).isoformat()+"Z",
    },
    {
      "desc": "Coffee",
      "category": "Caffeine",
      "color": "#795548",
      "start": (now - timedelta(hours=16)).isoformat()+"Z",
      "end":   (now - timedelta(hours=15, minutes=50)).isoformat()+"Z",
    },
    {
      "desc": "Lunch",
      "category": "Eating & Drinking",
      "color": "#f44336",
      "start": (now - timedelta(hours=12)).isoformat()+"Z",
      "end":   (now - timedelta(hours=11, minutes=30)).isoformat()+"Z",
    },
    {
      "desc": "Afternoon Gym",
      "category": "Exercise",
      "color": "#9c27b0",
      "start": (now - timedelta(hours=8)).isoformat()+"Z",
      "end":   (now - timedelta(hours=7, minutes=0)).isoformat()+"Z",
    },
    {
      "desc": "Night Sleep",
      "category": "Sleep",
      "color": "#3f51b5",
      "start": (now - timedelta(hours=2)).isoformat()+"Z",
      "end":   (now + timedelta(hours=6)).isoformat()+"Z",
    }
]
