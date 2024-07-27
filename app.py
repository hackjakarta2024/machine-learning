from flask import Flask, request, jsonify
import os
import json
from google.cloud import bigquery
from google.oauth2 import service_account
import schedule
import time
from datetime import datetime
import pandas as pd
import threading

app = Flask(__name__)

#create endpoint get /
# @app.route('/')
# def hello():
#     return "Hello World!"

#create endpoint post /recommend with return of dummy data already define in json format
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    if 'user_id' not in data:
        return jsonify({"status": "failure", "message": "user_id not provided"}), 400
    
    #define time based on current time breakfast (5-11), lunch (11-15), teatime (15-18), dinner (18-22), supper (22-5)
    current_hour = datetime.now().hour
    if current_hour >= 5 and current_hour < 11:
        period = 'breakfast'
    elif current_hour >= 11 and current_hour < 15:
        period = 'lunch'
    elif current_hour >= 15 and current_hour < 18:
        period = 'teatime'
    elif current_hour >= 18 and current_hour < 22:
        period = 'dinner'
    else:
        period = 'supper'

    user_id = data['user_id']
    return jsonify({
        "status": "success",
        "data": {
            "user_id": user_id,
            "promo_id": "2e6f4c5c-85va-4cd6-85f2-6d5f6a4d7c5f",
            "period": period,
            "food_recommendations": [
                {
                    "food_id": "2e6f4c2c-85ea-4cd6-85f2-6d5f6a4d7c5f",
                    "description": "Nasi Goreng",
                },
                {
                    "food_id": "2e6f4c2c-85ea-4cd6-84f2-6d5f6a4d7c5f",
                    "description": "Mie Goreng",
                },
                {
                    "food_id": "2e6f4c2c-85ea-4cd6-83f2-6d5f6a4d7c5f",
                    "description": "Ayam Goreng",
                },
                {
                    "food_id": "2e6f4c2c-85ea-4cd6-82f2-6d5f6a4d7c5f",
                    "description": "Nasi Goreng Seafood",
                },
                {
                    "food_id": "2e6f4c2c-85ea-4cd6-81f2-6d5f6a4d7c5f",
                    "description": "Nasi Goreng Ayam",
                },
                {
                    "food_id": "2e6f4c2c-85ea-4cd6-80f2-6d5f6a4d7c5f",
                    "description": "Nasi Goreng Seafood",
                },
                {
                    "food_id": "2e6f4c2c-85ea-4cd6-79f2-6d5f6a4d7c5f",
                    "description": "Nasi Goreng Ayam",
                },
                {
                    "food_id": "2e6f4c2c-85ea-4cd6-78f2-6d5f6a4d7c5f",
                    "description": "Nasi Goreng Seafood",
                },
                {
                    "food_id": "2e6f4c2c-85ea-4cd6-77f2-6d5f6a4d7c5f",
                    "description": "Nasi Goreng Ayam",
                },
                {
                    "food_id": "2e6f4c2c-85ea-4cd6-76f2-6d5f6a4d7c5f",
                    "description": "Nasi Goreng Seafood",
                }
            ]
        }
    })

def save_to_bigquery(data, target_project, target_dataset, target_table):
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE", ## overwrite
    )
    client = bigquery.Client(project=target_project)
    dataset_ref = client.dataset(target_dataset)
    table_ref = dataset_ref.table(target_table)
    job = client.load_table_from_dataframe(data, table_ref, location="asia-southeast2", job_config=job_config)
    result = job.result() # wait for the job to complete then proceed next code
    print("Data saved to BigQuery successfully.")
    return result 

#function write ke bq table using cron job, authentication using GOOGLE_APPLICATION_CREDENTIALS. cron job will running every hour and there will be a logic to define variable time = {breakfast(5.00), lunch(11.00), teatime (15.00), dinner(18.00), supper (22.00)} based on current time
@app.route('/')
def write_to_bq():
    #define time based on current time breakfast (5-11), lunch (11-15), teatime (15-18), dinner (18-22), supper (22-5)
    current_hour = datetime.now().hour
    if current_hour >= 5 and current_hour < 11:
        period = 'breakfast'
    elif current_hour >= 11 and current_hour < 15:
        period = 'lunch'
    elif current_hour >= 15 and current_hour < 18:
        period = 'teatime'
    elif current_hour >= 18 and current_hour < 22:
        period = 'dinner'
    else:
        period = 'supper'

    # Define the project ID
    project_id = 'hack-jakarta'

    # Define the data to be inserted for multiple user and each user have 10 food recommendations
    data = [
        {
            'user_id': 'user1',
            'promo_id': '2e6f4c5c-85va-4cd6-85f2-6d5f6a4d7c5f',
            'period': period,
            'food_recommendations': [
                {
                    'food_id': '2e6f4c2c-85ea-4cd6-85f2-6d5f6a4d7c5f',
                    'description': 'Nasi Goreng',
                },
                {
                    'food_id': '2e6f4c2c-85ea-4cd6-84f2-6d5f6a4d7c5f',
                    'description': 'Mie Goreng',
                },
                {
                    'food_id': '2e6f4c2c-85ea-4cd6-83f2-6d5f6a4d7c5f',
                    'description': 'Ayam Goreng',
                },
                {
                    'food_id': '2e6f4c2c-85ea-4cd6-82f2-6d5f6a4d7c5f',
                    'description': 'Nasi Goreng Seafood',
                },
                {
                    'food_id': '2e6f4c2c-85ea-4cd6-81f2-6d5f6a4d7c5f',
                    'description': 'Nasi Goreng Ayam',
                },
                {
                    'food_id': '2e6f4c2c-85ea-4cd6-80f2-6d5f6a4d7c5f',
                    'description': 'Nasi Goreng Seafood',
                },
                {
                    'food_id': '2e6f4c2c-85ea-4cd6-79f2-6d5f6a4d7c5f',
                    'description': 'Nasi Goreng Ayam',
                },
                {
                    'food_id': '2e6f4c2c-85ea-4cd6-78f2-6d5f6a4d7c5f',
                    'description': 'Nasi Goreng Seafood',
                },
                {
                    'food_id': '2e6f4c2c-85ea-4cd6-77f2-6d5f6a4d7c5f',
                    'description': 'Nasi Goreng Ayam',
                },
                {
                    'food_id': '2e6f4c2c-85ea-4cd6-76f2-6d5f6a4d7c5f',
                    'description': 'Nasi Goreng Seafood',
                }
            ]
        },
        {
            'user_id': 'user2',
            'promo_id': '2e6f4c5c-85va-4cd6-85f2-6d5f6a4d7c5f',
            'period': period,
            'food_recommendations': [
                {
                    'food_id': '2e6f4c2c-85ea-4cd6-85f2-6d5f6a4d7c5f',
                    'description': 'Nasi Goreng',
                },
                {
                    'food_id': '2e6f4c2c-85ea-4cd6-84f2-6d5f6a4d7c5f',
                    'description': 'Mie Goreng',
                },
                {
                    'food_id': '2e6f4c2c-85ea-4cd6-83f2-6d5f6a4d7c5f',
                    'description': 'Ayam Goreng',
                },
                {
                    'food_id': '2e6f4c2c-85ea-4cd6-82f2-6d5f6a4d7c5f',
                    'description': 'Nasi Goreng Seafood',
                },
                {
                    'food_id': '2e6f4c2c-85ea-4cd6-81f2-6d5f6a4d7c5f',
                    'description': 'Nasi Goreng Ayam',
                },
                {
                    'food_id': '2e6f4c2c-85ea-4cd6-80f2-6d5f6a4d7c5f',
                    'description': 'Nasi Goreng Seafood',
                },
                {
                    'food_id': '2e6f4c2c-85ea-4cd6-79f2-6d5f6a4d7c5f',
                    'description': 'Nasi Goreng Ayam',
                },
                {
                    'food_id': '2e6f4c2c-85ea-4cd6-78f2-6d5f6a4d7c5f',
                    'description': 'Nasi Goreng Seafood',
                },
                {
                    'food_id': '2e6f4c2c-85ea-4cd6-77f2-6d5f6a4d7c5f',
                    'description': 'Nasi Goreng Ayam',
                },
                {
                    'food_id': '2e6f4c2c-85ea-4cd6-76f2-6d5f6a4d7c5f',
                    'description': 'Nasi Goreng Seafood',
                }
            ]
        }
    ]
    # Flatten the data
    flattened_data = pd.DataFrame(data)
    save_to_bigquery(flattened_data, 'hack-jakarta', 'hackjakarta', 'recommendation')
    
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

#schedule cron job to run every hour
schedule.every(15).seconds.do(write_to_bq)

# Start the schedule in a separate thread
t = threading.Thread(target=run_schedule)
# Set the thread as daemon so it will end when the main program ends
t.setDaemon(True)
t.start()

if __name__ == '__main__':
    app.run( debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 3000)) )