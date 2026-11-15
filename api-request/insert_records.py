import os
import psycopg2
from api_request import mock_fetch_data,fetch_data

#connection to the db
def connect_to_db():
    print("CONNECTING to the PostgreSQL database.........")
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "db"),
            port=int(os.getenv("POSTGRES_PORT", 5432)),
            dbname=os.getenv("POSTGRES_DB", "db"),
            user=os.getenv("POSTGRES_USER", "db_user"),
            password=os.getenv("POSTGRES_PASSWORD", "db_password"),
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection failed:{e}")
        raise


def create_table(conn):
    print("Creating table if not exist....")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS dev;
            CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
                id  SERIAL PRIMARY KEY,
                city TEXT,
                temperature FLOAT,
                weather_Descriptions TEXT,
                wind_speed FLOAT,
                time TIMESTAMP,
                inserted_at TIMESTAMP DEFAULT NOW(),
                utc_offset TEXT
            );
        """)
        conn.commit()
        print("TABLE was created.")
    except psycopg2.Error as e:
        print(f"Failed to create table:{e}")
        raise

def insert_records(conn,data):
    print("Inserting weather data into the database...")
    try:
        weather = data['current']
        location = data ['location']
        cursor = conn.cursor()
        cursor.execute("""
           INSERT INTO dev.raw_weather_data(
               
               city,
               temperature,
               weather_descriptions,
               wind_speed,
               time,
               inserted_at,
               utc_offset
           ) VALUES(%s,%s,%s,%s,%s,NOW(),%s)
        
        
        """,(
            location['name'],
            weather['temperature'],
            weather['weather_descriptions'][0],
            weather['wind_speed'],
            location['localtime'],
            location['utc_offset']
        ))
        conn.commit()
        print("Data successfully inserted")
    except psycopg2.Error as e:
        print(f"Error inserting data into the database:{e}")
        raise

def main():
    try:
        #data = mock_fetch_data()
        data = fetch_data()
        conn = connect_to_db()    
        create_table(conn)
        insert_records(conn,data)          
    except Exception as e:
        print(f"An error occurred during execution:{e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("Database connection closed.")

#main()