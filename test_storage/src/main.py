from clickhouse.generate_data import run_clickhouse
from clickhouse.benchmark import start_test_clickhouse

from vertica.generate_data import run_vertica
from vertica.benchmark import start_test_vertica

import time

if __name__ == "__main__":
    start = time.time()
    run_clickhouse()
    print("insert_clickhouse", time.time() - start)
    start = time.time()
    run_vertica()
    print("insert_vertica", time.time() - start)

    start_test_clickhouse()
    start_test_vertica()
