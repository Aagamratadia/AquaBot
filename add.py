import mysql.connector
import random
from datetime import datetime, timedelta

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Aagam@03',
    'database': 'sewage_robot_data',
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS sewage_robot_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plastic_particles INT,
    saline_level FLOAT,
    temperature FLOAT,
    ph_level FLOAT,
    sensor_data VARCHAR(255),
    corrosion_level FLOAT,
    timestamp TIMESTAMP
);
"""
cursor.execute(create_table_query)
connection.commit()

# Add 100 random rows to the table
for _ in range(100):
    plastic_particles = random.randint(0, 100)
    saline_level = random.uniform(0.0, 1.0)
    temperature = random.uniform(0.0, 100.0)
    ph_level = random.uniform(0.0, 14.0)
    sensor_data = 'Random Sensor Data'
    corrosion_level = random.uniform(0.0, 100.0)
    timestamp = datetime.now() - timedelta(days=random.randint(0, 365))

    insert_query = """
    INSERT INTO sewage_robot_data (plastic_particles, saline_level, temperature, ph_level, sensor_data, corrosion_level, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (plastic_particles, saline_level, temperature, ph_level, sensor_data, corrosion_level, timestamp))

connection.commit()
connection.close()
