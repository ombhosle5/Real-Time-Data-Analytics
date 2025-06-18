from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType
import psycopg2  # PostgreSQL Connection
import time
import json

# Initialize Spark Session
spark = SparkSession.builder.appName("Wikimedia JSON Consumer").getOrCreate()

# Define Schema for JSON Data
schema = StructType().add("user", StringType(), True).add("title", StringType(), True).add("timestamp", StringType(), True)

# JSON file path (auto-updated by producer)
json_file = "real_time_data.json"

# PostgreSQL Connection Details
PG_HOST = "localhost"  # Change if needed
PG_DB = "postgres"    # Your database name
PG_USER = "postgres"    # Your username
PG_PASSWORD = "1111"  # Your password

# Connect to PostgreSQL
def connect_db():
    return psycopg2.connect(host=PG_HOST, database=PG_DB, user=PG_USER, password=PG_PASSWORD)

def store_in_db(data):
    """Inserts data into PostgreSQL."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO wikimedia_edits (username, title, timestamp)
            VALUES (%s, %s, %s)
        """
        cursor.executemany(insert_query, data)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Database Error: {e}")

# Track last read position
offset = 0  # Keeps track of how many rows have been processed
batch_size = 20  # Number of rows to read per batch
message_count = 0  # Counter for messages

def read_json_stream():
    """ Reads, displays, and stores new JSON data in PostgreSQL """
    global offset, message_count
    while True:
        try:
            df = spark.read.option("multiline", "true").json(json_file, schema=schema)
            total_rows = df.count()
            
            if total_rows > offset:
                new_df = df.limit(offset + batch_size).subtract(df.limit(offset))
                if new_df.count() > 0:
                    new_df.show(truncate=False)  # Display in console
                    store_in_db(new_df.collect())  # Store in PostgreSQL
                    message_count += new_df.count()  # Increment message count
                    print(f"Total Messages Processed: {message_count}")
                    offset += batch_size  # Update offset to next batch
                else:
                    print("No new data available.")
        except Exception as e:
            print(f"Waiting for data... {str(e)}")
        time.sleep(1)  # Check for updates every 5 seconds

if __name__ == "__main__":
    read_json_stream()
