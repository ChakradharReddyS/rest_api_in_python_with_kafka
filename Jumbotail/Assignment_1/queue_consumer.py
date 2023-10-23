import time
import psycopg2
from confluent_kafka import Consumer, KafkaException
import json


# Database connection settings
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "chakradhar"
DB_USER = "chakradhar"
DB_PASSWORD = "1234"

# Kafka consumer configuration
kafka_config = {
    'bootstrap.servers': 'localhost:9092', 
    'group.id': 'event-consumer',
    'auto.offset.reset': 'earliest',  # Set to 'earliest' to start from the beginning of the topic
}
kafka_consumer = Consumer(kafka_config)
kafka_consumer.subscribe(['events-topic1'])  # Subscribe to the Kafka topic

# Function to insert events into the database
def insert_events(events):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        for event in events:
            # Create a events_table if it does not exist 
            # Inserting events into my database table.
            sql = """CREATE TABLE IF NOT EXISTS app_events_table_v2 (
                    event_timestamp BIGINT,
                    user_id INTEGER,
                    event_type VARCHAR(255),
                    city VARCHAR(20)
                   );
                   INSERT INTO app_events_table_v2 (event_timestamp, user_id, event_type, city) VALUES (%s, %s, %s, %s)"""
            data = (event['timestamp'], event['user_id'], event['event_type'], event['city'])
            cursor.execute(sql, data)

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error inserting events into the database: {str(e)}")
        return False

def queue_consumer():
    try:
        while True:
            batch = []
            for i in range(BATCH_SIZE):
                # Poll for events from Kafka
                msg = kafka_consumer.poll(1.0)  # Adjust the timeout as needed
            
                if msg is None:
                    continue
            
                if msg.error():
                    raise KafkaException(msg.error())
                else:
                    event_str = msg.value().decode('utf-8')
                    # Deserialize the event (e.g., JSON parsing)
                    event_str = event_str.replace("'",'"')
                    event = json.loads(event_str)
                    batch.append(event)

            if batch:
                if insert_events(batch):
                    print(f"Inserted {len(batch)} events into the database.")
                else:
                    print("Failed to insert events into the database. Retrying...")
                    # You can implement a retry mechanism here.

            time.sleep(1)  # Sleep for a while before processing the next batch

    except KeyboardInterrupt:
        print('Canceled by user')



if __name__ == "__main__":
    #app.run(host='localhost', port=8888, threaded=True)
    BATCH_SIZE = 10  # Adjust batch size as needed
    queue_consumer()
