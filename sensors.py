# sensors.py
import random
from datetime import datetime, timedelta
from collections import deque

# Event definitions
events_timeline = [
    {"type": "meal",    "desc": "Breakfast",  "start": -2,  "duration": 30},  # hours ago, minutes
    {"type": "coffee",  "desc": "Coffee",    "start": -3,  "duration": 15},
    {"type": "exercise","desc": "Gym",       "start": -20, "duration": 60},
    {"type": "sleep",   "desc": "Night Sleep","start": -13, "duration": 480},
    {"type": "meal",    "desc": "Lunch",      "start": -24,"duration": 45},
    {"type": "exercise","desc": "Walk",      "start": -16,"duration": 30},
    {"type": "meal",    "desc": "Dinner",     "start": -18,"duration": 60},
]

def _event_active(now, event):
    # computes minutes since event started: negative if in future
    start_time = now + timedelta(hours=event['start'])
    end_time = start_time + timedelta(minutes=event['duration'])
    return start_time <= now <= end_time

# baseline and state
BASELINE = {
    'glucose': 90,
    'lactate': 1.0,
    'heart_rate': 65,
    'skin_temp': 34.5,
    'gsr': 2.5,
}
# keep last 5 values for simple smoothing
_history = {k: deque([v]*5, maxlen=5) for k,v in BASELINE.items()}

# produce 24h history buffer
historical_data = []

def generate_sensor_data(timestamp=None):
    now = datetime.utcnow()
    if timestamp is None:
        timestamp = now.isoformat() + 'Z'
        ts = now
    else:
        ts = datetime.fromisoformat(timestamp.replace('Z',''))

    state = {}
    # simulate each sensor with event effects + decay + smoothing
    # glucose: rises after meals
    g = BASELINE['glucose']
    for ev in events_timeline:
        if _event_active(ts, ev) and ev['type']=='meal':
            g += 30
    # gradual decay
    g = g - (now - ts).total_seconds()/3600*5
    _history['glucose'].append(g)
    state['glucose'] = sum(_history['glucose'])/len(_history['glucose'])

    # lactate: spikes during exercise
    l = BASELINE['lactate']
    for ev in events_timeline:
        if _event_active(ts, ev) and ev['type']=='exercise':
            l += 2
    _history['lactate'].append(l)
    state['lactate'] = sum(_history['lactate'])/len(_history['lactate'])

    # heart rate: increases with exercise and caffeine
    hr = BASELINE['heart_rate']
    for ev in events_timeline:
        if _event_active(ts, ev) and ev['type'] in ('exercise','coffee'):
            hr += 20
    _history['heart_rate'].append(hr)
    state['heart_rate'] = sum(_history['heart_rate'])/len(_history['heart_rate'])

    # skin temp: slight rise with exercise
    st = BASELINE['skin_temp']
    for ev in events_timeline:
        if _event_active(ts, ev) and ev['type']=='exercise':
            st += 0.5
    _history['skin_temp'].append(st)
    state['skin_temp'] = sum(_history['skin_temp'])/len(_history['skin_temp'])

    # GSR: changes with caffeine and stress events
    gsr = BASELINE['gsr']
    for ev in events_timeline:
        if _event_active(ts, ev) and ev['type']=='coffee':
            gsr += 1
    _history['gsr'].append(gsr)
    state['gsr'] = sum(_history['gsr'])/len(_history['gsr'])

    # package
    return {
        'timestamp': timestamp,
        'sensor': state,
        'active_events': [ev['desc'] for ev in events_timeline if _event_active(ts, ev)]
    }

# initialize historical_data
ts0 = datetime.utcnow() - timedelta(hours=24)
for i in range(int(24*60/5)):
    ts = ts0 + timedelta(minutes=5*i)
    data = generate_sensor_data(ts.isoformat()+'Z')
    historical_data.append(data)
