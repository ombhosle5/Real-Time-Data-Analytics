from kafka import KafkaProducer
import requests
import json
import time

WIKIMEDIA_URL = "https://stream.wikimedia.org/v2/stream/recentchange"
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

JSON_FILE = "real_time_data.json"  # File to store real-time updates

def write_to_json(event_data):
    """ Append new event data to a JSON file """
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []  # If the file doesn't exist or is empty, initialize as an empty list

    existing_data.append(event_data)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4)

def stream_and_send():
    with requests.get(WIKIMEDIA_URL, stream=True) as response:
        for line in response.iter_lines():
            if line and line.startswith(b'data:'):
                data_str = line.decode('utf-8')[6:]
                event_data = json.loads(data_str)

                clean_message = f"User {event_data.get('user', 'Unknown User')} edited page: {event_data.get('title', 'Unknown Page')} at {event_data.get('timestamp', 'Unknown Time')}"
                print(clean_message)

                # Send data to Kafka topic
                producer.send('wikimedia-events', value=event_data)

                # Save data to JSON file
                write_to_json(event_data)

                time.sleep(0)  # Simulating real-time streaming

if __name__ == "__main__":
    stream_and_send()
