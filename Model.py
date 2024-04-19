import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector
import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def get_plastic_amount():
    # Replace this with the actual method to get the plastic amount from your data
    return 96
def get_corrosion_prediction(date):
    # Replace this with the actual method to predict corrosion levels on a given date
    return 92.5

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Aagam@03',
    'database': 'parkinglot',
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS parking_rec (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_number VARCHAR(20),
    vehicle_type VARCHAR(20),
    checkin_date DATE,
    checkin_time TIME
);
"""
cursor.execute(create_table_query)
connection.commit()

def get_predicted_available_spaces():
    query = "SELECT checkin_date, available_cars FROM parking_rec"
    df = pd.read_sql_query(query, connection)

    df['checkin_date'] = pd.to_datetime(df['checkin_date'])
    df['day_of_week'] = df['checkin_date'].dt.day_name()
    df['month'] = df['checkin_date'].dt.month
    df = pd.get_dummies(df, columns=['day_of_week'])

    X = df.drop(['checkin_date', 'available_cars'], axis=1)
    y = df['available_cars']

    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    future_date = datetime.strptime('2023-12-15', '%Y-%m-%d')
    future_day_of_week = future_date.strftime('%A')
    future_month = future_date.month

    future_data = pd.get_dummies(pd.DataFrame({
        'month': [future_month],
        'day_of_week': [future_day_of_week]
    }), columns=['day_of_week'])

    missing_columns = set(X_train.columns) - set(future_data.columns)
    for col in missing_columns:
        future_data[col] = 0

    future_data = future_data[X_train.columns]

    predicted_available_spaces = model.predict(future_data)
    return f"Pipe burst expected at MUM_DICT1 at {future_date}:with probablity {predicted_available_spaces[0]}"

def show_prediction_result():
    result_label.config(text=get_predicted_available_spaces())

    plastic_amount = get_plastic_amount()
    if plastic_amount > 95:
        messagebox.showinfo("Plastic Alert", f"Plastic level is {plastic_amount}%. Take necessary action!")


root = tk.Tk()
root.title("Sewage Pipe prediction")


result_label = ttk.Label(root, text="")
result_label.pack(pady=10)


predict_button = ttk.Button(root, text="Show Prediction Result", command=show_prediction_result)
predict_button.pack(pady=10)

root.mainloop()
