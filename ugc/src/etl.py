import logging
import json
import os
import time
from core.config import GeneralConfig
from kafka import KafkaConsumer
from clickhouse_driver import Client
from typing import Dict, List, Any
from pathlib import Path
from schemas.request.event import EventModel

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="logs_etl.log",
    filemode="a+",
)

config = GeneralConfig()


class KafkaToClickHouseETL:
    def __init__(self):

        self.consumer = KafkaConsumer(
            config.TOPIC_KAFKA,
            group_id="etl_group",
            bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
            enable_auto_commit=False,
        )

        self.clickhouse_client = Client(
            host=config.CLICKHOUSE_HOST,
            database=config.CLICKHOUSE_DATABASE,
            user=config.CLICKHOUSE_USER,
            password=config.CLICKHOUSE_PASSWORD,
        )

    def extract(self) -> List[Dict[str, Any]]:
        messages = []
        try:
            while True:
                received_msgs = self.consumer.poll(
                    timeout_ms=10, max_records=config.BATCH_SIZE
                )
                if not received_msgs:
                    break
                for topic_partition, partition_messages in received_msgs.items():
                    for message in partition_messages:
                        decoded_msg = json.loads(message.value.decode("utf-8"))
                        messages.append(decoded_msg)
        except Exception as e:
            logging.error(f"error: {e}")
        return messages

    def get_transformed_data(self, raw_data: List[str]) -> List[Dict[str, Any]]:
        transformed_data = []

        for item in raw_data:
            try:
                validated_event = EventModel(**item)
                validated_event.content = {
                    k: str(v) for k, v in validated_event.content.items()
                }
                transformed_data.append(validated_event.model_dump())

            except ValidationError as ve:
                logger.error(f"Ошибка валидации данных '{item}': {ve}")
            except Exception as e:
                logging.error(f"Ошибка при обработке данных: {e}")

        return transformed_data

    def load(self, data: List[Dict[str, Any]]):
        try:
            self.clickhouse_client.execute("INSERT INTO UGC_table VALUES", data)
            logging.info("Данные успешно загружены в ClickHouse")
            self.consumer.commit()
        except Exception as e:
            logging.error(f"Ошибка при загрузке данных в ClickHouse: {e}")

    def run(self):
        while True:
            raw_data = self.extract()
            if raw_data:
                transformed_data = self.get_transformed_data(raw_data)
                if transformed_data:
                    self.load(transformed_data)
            time.sleep(5)


if __name__ == "__main__":
    connection = False
    while not connection:
        try:
            etl_process = KafkaToClickHouseETL()
            connection = True
        except:
            pass
        time.sleep(2)
    etl_process.run()
