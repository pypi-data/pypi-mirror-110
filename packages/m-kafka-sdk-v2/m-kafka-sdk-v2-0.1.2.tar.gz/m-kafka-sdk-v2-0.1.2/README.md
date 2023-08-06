- **Thư viện Consumer của JB. Chạy consumer ở Process, phù hợp cho môi trường K8s** :

```python
import os
from time import sleep
from pymongo import MongoClient
from mobio.libs.kafka_lib.helpers.kafka_consumer_manager import BaseKafkaConsumer


class TestConsumer(BaseKafkaConsumer):
    def message_handle(self, data):
        print("TestConsumer: data: {}".format(data))


if __name__ == "__main__":
    url_connection = os.getenv('TEST_MONGO_URI')
    client_mongo = MongoClient(url_connection, connect=False)

    TestConsumer(topic="test", group_id="test", client_mongo=client_mongo, retryable=False)
    sleep(1000)
```
* 0.1.1: fix bug init Config