# rest_api_in_python_with_kafka
Developed a REST API for E-Commerce application that is used for data transfer from app to database by using Kafka as message queue system


# Complete Setup

## Setting up Python  Environment


1) Create a folder named ‘RESTAPI_in_Python’ on desktop

2) Install the python3-venv package using the following command

```bash
sudo apt install python3.10-env
```

3) Open the above folder in VSCode and create a python virtual environment

```bash
python3 -m venv .venv
```

4) Kill and restart the terminal. Navigate to the code directory and enter below command to enter python  virtual environment

```bash
source .venv/bin/activate
```

## Event Producer

The Event Producer simulates users generating events. In a real scenario, these events would be generated by user actions. For simplicity, we'll generate random events in this example.

1) Create a file named ‘event_producer.py’
  
2) Install requests library using pip command in python virtual environment 

```bash
pip install requests
```

> The requests library in Python is a popular library for making HTTP requests

3) Add the following import statements at the top of the ‘event_producer.py file:

 ```python
import threading
import requests
import random
import time
```

> **threading**  - To implement multithreading in driver class
> **requests**  -  for making HTTP requests
> **random**    - Provides function to simulate event generation
> **time**         - takes snapshots of system clocks. Used for measuring the response time

4) Generate events using the **random.choices()** function as below

```python
# Function to generate events
def generate_event(user_id):
    event_type = random.choices(EVENT_TYPES, EVENT_PROBABILITIES)[0]
    city = random.choice(INDIAN_CITIES)
    return {"timestamp": time.time(), "user_id": user_id, "event_type": event_type, "city": city}
```

In the above code, random.choices(EVENT_TYPES,EVENT_PROBABILITIES)[0] is used to randomly select an event type from the list of EVENT_TYPES based on the given probabilities in EVENT_PROBABILITIES. The event_probabilities here account for user behaviour


## WebHook

The Webhook acts as a receiver for events generated by the Event Producer. It accepts incoming event payloads and pushes them to an In-memory Queue(Kafka) for processing.

1) Navigate to the virtual environment
  
2) Install flask using pip command
```bash
pip install flask
```

3) Install confluent_kafka using pip command          
```bash           
pip install confluent-kafka
```

4) Create a file named ‘webhook.py’

5) Import Producer class into webhook python file to write events to a Kafka topic
```python
from confluent_kafka import Producer
```

## Kafka (In-Memory Queue)

The main objective of the queue is to enable asynchronous behavior. In the context of our webhook API, events will be pushed into this in-memory queue, and a consumer will retrieve the events from the queue to ultimately insert them into a database of your preference.

1) Download Kafka from official Apache Kafka web page onto your local device and extract the contents of tar file

2) Navigate to the kafka directory(‘downloads/kafka_2.12-3.6.0’) and start zookeeper server using below command
```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

3) After Zookeper server is running, Start Kafka Server in another terminal window using the command below
```bash
bin/kafka-server-start.sh config/server.properties
```

4) After zookeeper and Kafka services are running, create a Kafka topic
```bash 
bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic events-topic1
```

## Queue Consumer

The Queue Consumer is responsible for retrieving messages from the in-memory queue in batches and inserting them into the database of your choice.

1) Navigate to the virtual environment 

2) Install Postgres and PgAdmin on your device 

3) Install psycopg2 using pip command to interact with PostgreSQL databases
```bash
pip install psycopg2-binary
```

4) Open psql terminal from Postgres app and type \conninfo to get the database connection parameters

5) Create a Python file 'queue_consumer.py'    

6) Import the Consumer class from confluent_kafka module to read events from a Kafka topic
```python
from confluent_kafka import Consumer
```



# Execution

## Run the components

Run all the components in the Python Virtual Environment as all the python modules/libraries are installed in this virtual env

1) Start the Webhook:
```bash
python3 webhook.py
```

2) Start the Queue Consumer:
```bash
python3 queue_consumer.py
```

3) Start the Event Producer:
```bash
python3 event_producer.py
```

Your API will now accept incoming event payloads asynchronously, store them in the in-memory queue, and have a queue consumer process to retrieve events from in-memory queue and to store the events in a database for analysis
   





