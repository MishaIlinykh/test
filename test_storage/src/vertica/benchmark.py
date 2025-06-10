import vertica_python
import threading
import time


def start_test_vertica():
    conn_info = {
        "host": "vertica",
        "port": 5433,
        "user": "dbadmin",
        "password": "",
        "database": "docker",
    }

    def run_query():
        with vertica_python.connect(**conn_info) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT event_type, COUNT(*), AVG(value) FROM events GROUP BY event_type"
            )
            result = cur.fetchall()
            # print(result)

    threads = [threading.Thread(target=run_query) for _ in range(8)]
    start = time.time()
    [t.start() for t in threads]
    [t.join() for t in threads]
    print(f"Vertica Total time: {time.time() - start:.2f}s")
