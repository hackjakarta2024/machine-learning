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
                    "food_id": "a8e9bce3-3444-4904-a7f5-a89b7d30735c",
                    "description": "Nasi Goreng",
                },
                {
                    "food_id": "59f90db3-d84f-4509-a088-93f7a2857e3e",
                    "description": "Mie Goreng",
                },
                {
                    "food_id": "dd4c3b19-a4fb-40ea-8cb0-fb4c2fdbdcbd",
                    "description": "Ayam Goreng",
                },
                {
                    "food_id": "6b300f18-a057-4b92-84e0-7fa7ac10891e",
                    "description": "Nasi Goreng Seafood",
                },
                {
                    "food_id": "35abfb33-ed29-4c29-9cfb-7827937e158f",
                    "description": "Nasi Goreng Ayam",
                },
                {
                    "food_id": "8f698978-1b45-4f1f-9663-d02adfb050a5",
                    "description": "Nasi Goreng Seafood",
                },
                {
                    "food_id": "010c0ec5-0f30-47ec-85f3-0aa945ed0d9f",
                    "description": "Nasi Goreng Ayam",
                },
                {
                    "food_id": "0d742318-ad53-4596-b68f-a53f5f616686",
                    "description": "Nasi Goreng Seafood",
                },
                {
                    "food_id": "cac16bd8-392a-4817-ac7c-196acada111b",
                    "description": "Nasi Goreng Ayam",
                },
                {
                    "food_id": "588c487c-d496-4560-b2a5-a38a7871be1b",
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

#read from params user_id and query for endpoint search and return dummy data
@app.route('/search')
def search():
    user_id = request.args.get('user_id')
    query = request.args.get('query')
    if not user_id:
        return jsonify({"status": "failure", "message": "user_id not provided"}), 400
    #read from query and print it
    print(user_id)
    print(query)
    return jsonify({
        "status": "success",
        "data": {
            "user_id": "290fbc73-84f1-4a09-aa1f-1b09bbc2539e",
            "food_recommendations": [
                {
                    "food_id": "a8e9bce3-3444-4904-a7f5-a89b7d30735c",
                    "desc": "Nasi Goreng",
                },
                {
                    "food_id": "59f90db3-d84f-4509-a088-93f7a2857e3e",
                    "desc": "Mie Goreng",
                },
                {
                    "food_id": "dd4c3b19-a4fb-40ea-8cb0-fb4c2fdbdcbd",
                    "desc": "Ayam Goreng",
                },
                {
                    "food_id": "6b300f18-a057-4b92-84e0-7fa7ac10891e",
                    "desc": "Nasi Goreng Seafood",
                },
                {
                    "food_id": "35abfb33-ed29-4c29-9cfb-7827937e158f",
                    "desc": "Nasi Goreng Ayam",
                },
                {
                    "food_id": "8f698978-1b45-4f1f-9663-d02adfb050a5",
                    "desc": "Nasi Goreng Seafood",
                },
                {
                    "food_id": "010c0ec5-0f30-47ec-85f3-0aa945ed0d9f",
                    "desc": "Nasi Goreng Ayam",
                },
                {
                    "food_id": "0d742318-ad53-4596-b68f-a53f5f616686",
                    "desc": "Nasi Goreng Seafood",
                },
                {
                    "food_id": "cac16bd8-392a-4817-ac7c-196acada111b",
                    "desc": "Nasi Goreng Ayam",
                },
                {
                    "food_id": "588c487c-d496-4560-b2a5-a38a7871be1b",
                    "desc": "Nasi Goreng Seafood",
                }
            ]
        }
    })
            


#function write ke bq table using cron job, authentication using GOOGLE_APPLICATION_CREDENTIALS. cron job will running every hour and there will be a logic to define variable time = {breakfast(5.00), lunch(11.00), teatime (15.00), dinner(18.00), supper (22.00)} based on current time
@app.route('/')
def write_to_bq():
    #define time based on current time breakfast (5), lunch (11), teatime (15), dinner (18), supper (22)
    current_hour = datetime.now().hour
    print("Current Hour: ", current_hour)
    if current_hour == 5:
        period = 'breakfast'
    elif current_hour == 11:
        period = 'lunch'
    elif current_hour == 15:
        period = 'teatime'
    elif current_hour == 18:
        period = 'dinner'
    elif current_hour == 22:
        period = 'supper'

    # Define the project ID
    project_id = 'hack-jakarta'

    # Define the data to be inserted for multiple user and each user have 10 food recommendations
    data = [
        {
            'user_id': '290fbc73-84f1-4a09-aa1f-1b09bbc2539e',
            'promo_id': '03990610-f220-4cf2-9e2e-e9b5f63f90ab',
            'period': period,
            'food_recommendations': [
                {
                    "food_id": "a8e9bce3-3444-4904-a7f5-a89b7d30735c",
                    "description": "Nasi Goreng",
                },
                {
                    "food_id": "59f90db3-d84f-4509-a088-93f7a2857e3e",
                    "description": "Mie Goreng",
                },
                {
                    "food_id": "dd4c3b19-a4fb-40ea-8cb0-fb4c2fdbdcbd",
                    "description": "Ayam Goreng",
                },
                {
                    "food_id": "6b300f18-a057-4b92-84e0-7fa7ac10891e",
                    "description": "Nasi Goreng Seafood",
                },
                {
                    "food_id": "35abfb33-ed29-4c29-9cfb-7827937e158f",
                    "description": "Nasi Goreng Ayam",
                },
                {
                    "food_id": "8f698978-1b45-4f1f-9663-d02adfb050a5",
                    "description": "Nasi Goreng Seafood",
                },
                {
                    "food_id": "010c0ec5-0f30-47ec-85f3-0aa945ed0d9f",
                    "description": "Nasi Goreng Ayam",
                },
                {
                    "food_id": "0d742318-ad53-4596-b68f-a53f5f616686",
                    "description": "Nasi Goreng Seafood",
                },
                {
                    "food_id": "cac16bd8-392a-4817-ac7c-196acada111b",
                    "description": "Nasi Goreng Ayam",
                },
                {
                    "food_id": "588c487c-d496-4560-b2a5-a38a7871be1b",
                    "description": "Nasi Goreng Seafood",
                }
            ]
        },
        {
            'user_id': '65add329-203e-43e0-816e-5f1915720e3b',
            'promo_id': '03990610-f220-4cf2-9e2e-e9b5f63f90ab',
            'period': period,
            'food_recommendations': [
                {
                    "food_id": "a8e9bce3-3444-4904-a7f5-a89b7d30735c",
                    "description": "Nasi Goreng",
                },
                {
                    "food_id": "59f90db3-d84f-4509-a088-93f7a2857e3e",
                    "description": "Mie Goreng",
                },
                {
                    "food_id": "dd4c3b19-a4fb-40ea-8cb0-fb4c2fdbdcbd",
                    "description": "Ayam Goreng",
                },
                {
                    "food_id": "6b300f18-a057-4b92-84e0-7fa7ac10891e",
                    "description": "Nasi Goreng Seafood",
                },
                {
                    "food_id": "35abfb33-ed29-4c29-9cfb-7827937e158f",
                    "description": "Nasi Goreng Ayam",
                },
                {
                    "food_id": "8f698978-1b45-4f1f-9663-d02adfb050a5",
                    "description": "Nasi Goreng Seafood",
                },
                {
                    "food_id": "010c0ec5-0f30-47ec-85f3-0aa945ed0d9f",
                    "description": "Nasi Goreng Ayam",
                },
                {
                    "food_id": "0d742318-ad53-4596-b68f-a53f5f616686",
                    "description": "Nasi Goreng Seafood",
                },
                {
                    "food_id": "cac16bd8-392a-4817-ac7c-196acada111b",
                    "description": "Nasi Goreng Ayam",
                },
                {
                    "food_id": "588c487c-d496-4560-b2a5-a38a7871be1b",
                    "description": "Nasi Goreng Seafood",
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
# schedule.every().hour.do(write_to_bq)

schedule.every(30).seconds.do(write_to_bq)

# Start the schedule in a separate thread
t = threading.Thread(target=run_schedule)
# Set the thread as daemon so it will end when the main program ends
t.setDaemon(True)
t.start()

if __name__ == '__main__':
    app.run( debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 3000)) )