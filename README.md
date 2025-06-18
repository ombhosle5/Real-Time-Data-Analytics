# Real-Time-Data-Analytics
Real-time data analytics using Apache Spark, Kafka, PostgreSQL, and Dash with Wikimedia stream.

# 📊 Real-Time Data Analytics using Apache Kafka and Apache Spark

This project demonstrates a real-time data analytics pipeline built with Apache Kafka, Apache Spark, and PostgreSQL, with interactive visualization using Dash and Plotly.

---

## 🚀 Project Overview

- Stream real-time data from Wikimedia’s public API using a Kafka producer.
- Process the data using Apache Spark in micro-batches.
- Store the processed data in a PostgreSQL database.
- Display live updates on a dynamic dashboard using Dash and Plotly.

---

## ⚙️ Tech Stack

- **Apache Kafka**: Real-time messaging system
- **Apache Spark**: Stream processing and analytics
- **PostgreSQL**: Data storage
- **Dash by Plotly**: Dashboard and visualization
- **Python**: Core programming language

---

## Project Data Flow 

Producer → real_time_data.json → Spark Consumer → PostgreSQL → Dashboard
           (intermediate buffer)       (processing)      (storage)    (visualization)

---
## Create and activate a virtual environment

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

---

## 📁 Project Structure

├── producer.py # Kafka producer streaming Wikimedia events
├── consumer.py # Spark consumer processing and storing events
├── dashboard.py # Dash app for visualization
├── real_time_data.json # Backup of streamed JSON data
├── requirements.txt # Python dependencies
└── README.md # This documentation

---

## 🧰 Requirements

Install dependencies using:
information provided in requirments.txt

Make sure you have:

Java (JDK 8 or 11)

Apache Kafka (running locally)

Apache Spark

PostgreSQL (with a table named wikimedia_edits)

---

## 📊 Dashboard Preview

Here is a snapshot of the real-time dashboard:

![Dashboard Preview](./image/Dashboard_output.jpg)


## How to Run step-by-step
1) Start Kafka and Zookeeper locally

2) Run the Kafka Producer
    python producer.py

##  You MUST Create real_time_data.json Before Running the Consumer

Why?
Your producer is writing the real-time stream data into real_time_data.json.
Your Spark-based consumer reads that file, parses it with a schema, and processes/stores the data.
If the file doesn't exist, Spark will throw an error saying “File not found or empty”.

🛠️ So before starting the consumer, just do:

echo "[]" > real_time_data.json
This creates an empty JSON array — the right structure for appending JSON objects in a list.

3) Run the Spark Consumer
    python consumer.py

4) It also storing data in PostgreSQL 

5) Run the Dashboard
    python dashboard.py

---

## 📚 References

Wikimedia API: "https://stream.wikimedia.org/v2/stream/recentchange"

Apache Kafka : "https://spark.apache.org/downloads.html"

Apache Spark : "https://kafka.apache.org/downloads"

PostgreSQL : "https://www.postgresql.org/"

---

## 👨‍💻 Author
Om Bhosle
-
*Versatile tech enthusiast with strong problem-solving and teamwork skills. Quick learner, adaptable, and eager to grow in dynamic tech environments.*
---
Let me know if you'd like me to customize the README even more (e.g., adding a project logo, PostgreSQL schema, etc.).
