from clickhouse_driver import Client
import threading
import time


def start_test_clickhouse():
    def run_query():
        client = Client(
            host="clickhouse-server", user="admin_user", password="strong_passw0rd!"
        )
        result = client.execute(
            "SELECT event_type, count(), avg(value) FROM events GROUP BY event_type"
        )
        # print(result)

    threads = [threading.Thread(target=run_query) for _ in range(8)]

    start = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"ClickHouse Total time: {time.time() - start:.2f}s")
