import vertica_python
from common.data_generator import generate_events


def run_vertica():
    conn_info = {
        "host": "vertica",
        "port": 5433,
        "user": "dbadmin",
        "password": "",
        "database": "docker",
    }

    with vertica_python.connect(**conn_info) as conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS events")
        cur.execute(
            """
            CREATE TABLE events (
                event_time TIMESTAMP,
                user_id INT,
                event_type VARCHAR(20),
                value FLOAT
            )
        """
        )

        data = list(generate_events(10_000_000))

        insert_query = "INSERT INTO events (event_time, user_id, event_type, value) VALUES (%s, %s, %s, %s)"
        cur.executemany(insert_query, [tuple(e.values()) for e in data])

        conn.commit()
