from confluent_kafka import Consumer
from database import insert_watched

consumer = Consumer(
    {
        "bootstrap.servers": "localhost:9092",
        "group.id": "consumer_service",
    }
)

consumer.subscribe(['watched'])


def check_message(message):
    if message is None:
        return False
    if message.error():
        return False


BATCH_SIZE = 100
while True:
    batch = consumer.consume(num_messages=BATCH_SIZE, timeout=1.0)
    if batch is None:
        continue

    for message in batch:
        if not check_message(message):
            continue

        message_value = message.value()
        user_id = message_value.get('user_id')
        video_id = message_value.get('video_id')

        insert_watched(user_id, video_id)

    consumer.commit(asynchronous=False)

consumer.close()
