import random
from datetime import datetime, timedelta


def generate_events(n=10_000_000):
    event_types = ["click", "view", "purchase"]
    start = datetime(2020, 1, 1)
    for _ in range(n):
        yield {
            "event_time": start + timedelta(seconds=random.randint(0, 10_000_000)),
            "user_id": random.randint(1, 1_000_000),
            "event_type": random.choice(event_types),
            "value": random.uniform(1.0, 100.0),
        }
