from clickhouse_driver import Client
from common.data_generator import generate_events


def run_clickhouse():

    client = Client(
        host="clickhouse-server", user="admin_user", password="strong_passw0rd!"
    )

    client.execute("DROP TABLE IF EXISTS events")
    client.execute(
        """
	    CREATE TABLE events (
	        event_time DateTime,
	        user_id UInt32,
	        event_type String,
	        value Float32
	    ) ENGINE = MergeTree()
	    ORDER BY event_time
	"""
    )

    data = list(generate_events(10_000_000))
    client.execute("INSERT INTO events VALUES", [tuple(e.values()) for e in data])
