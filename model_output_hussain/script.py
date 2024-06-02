"""
Main Live Script For Script of Scopium EKG

https://ekg.pythonanywhere.com/ekg/both_symtoms_prediction/?action=v1

Running Testcases and see on the live and cross-check the tests 


# Number of test cases
num_tests = 1500

"""

import requests
import json
import random
import time
from pprint import pprint
import pandas as pd
from pathlib import Path

result_dict = json.load(open("dict.json", "r"))
diseases = ['Aortic Dissection', 'AS/AI', 'CHF', 'Eso rupture', 'GI', 'infarct', 'Ischemia', 'MS', 'PE', 'Pericarditis', 'Pulmonary']


# Function to get random chest_pain_values and question_values for a given key
def get_random_values(user_key, num_values, result_dict):
    if user_key in result_dict:
        df_list = result_dict[user_key]
        # Check if the requested number of values is greater than the available entries
        num_values = min(num_values, len(df_list))
        # Randomly select 'num_values' entries
        random_entries = random.sample(df_list, num_values)

        age_count = 0
        filtered_entries = []

        for entry in random_entries:
            if 'Age' in entry['Chest Pain'] and age_count == 0:
                filtered_entries.append(entry)
                age_count += 1
            elif 'Age' not in entry['Chest Pain']:
                filtered_entries.append(entry)

        # inline loop
        # filtered_entries = [entry for entry in random_entries if ('Age' in entry['Chest Pain'] and (age_count := age_count + 1) == 1) or 'Age' not in entry['Chest Pain']]        
        return filtered_entries
    else:
        return None



## for checking the randomvalues Age only 1
# for i in range (50):
#     user_key = random.choice(diseases)
#     print("Input: ",user_key)
#     num_values = random.randint(5, 8)
#     print("num_values (5 to 8):  ",num_values)
#     print(get_random_values(user_key, num_values, result_dict))
    

# Number of test cases
num_tests = 3000

for test_num in range(1, num_tests + 1):
    # time.sleep(1)

    print(f"\n\n**************** START {test_num} ***********************")

    user_key = random.choice(diseases)
    print("Input: ",user_key)

    num_values = random.randint(5, 8)
    print("num_values (5 to 8):  ",num_values)

    random_values = get_random_values(user_key, num_values, result_dict)
    
    api_payload = {
            "all_symtoms": [{"id": entry['question'], "symtoms": entry['Chest Pain']} for entry in random_values],
            "current": [{"id": entry['question'], "symtoms": entry['Chest Pain']} for entry in random_values]
        }

    # Convert the payload to JSON
    api_payload_json = json.dumps(api_payload)

    url = "https://ekg.pythonanywhere.com/ekg/both_symtoms_prediction/?action=v1"
    headers = {'Content-Type': 'application/json'}
    # time.sleep(1)
    response = requests.post(url, headers=headers, data=api_payload_json, timeout=300)
    # time.sleep(2)
    
    response_json = response.json()

    all_data = []
    try:
        live_data = response_json["live"]["data"]
        beta_data = response_json["beta"]["data"]
    except KeyError:
        print("\n\n **************************************************************************************")
        print("\n\nERROR API and Payload  !!!!!!!!!!!!!!!")
        print("\n",url)
        print("\n",api_payload_json)
        print("\nResponse")
        print(json.dumps(response_json))
        print("\n\n **************************************************************************************")
        break


    live_top_diseases = [entry['diseases_name'] for entry in live_data[:2]]
    beta_top_diseases = [entry['diseases_name'] for entry in beta_data[:2]]

    print("live_top_diseases: ",live_top_diseases)
    print("beta_top_diseases: ", beta_top_diseases)

    # For matching must convert to lowercase
    user_key_lower = user_key.lower()
    live_top_diseases_lower = [desease.lower() for desease in live_top_diseases]
    beta_top_diseases_lower = [desease.lower() for desease in beta_top_diseases]

    status_live = "pass" if user_key_lower in live_top_diseases_lower else "fail"
    status_beta = "pass" if user_key_lower in beta_top_diseases_lower else "fail"

    print("Input: ",user_key)
    print("status_live: ", status_live)
    print('status_beta: ', status_beta)

    headers = ["live/beta", "desease", "status", "model_output", "symptoms"]
    row_live = ["live", user_key, status_live, ', '.join(desease for desease in live_top_diseases),  ', '.join(entry['Chest Pain'] for entry in random_values)]
    row_beta = ["beta", user_key, status_beta, ', '.join(desease for desease in beta_top_diseases),  ', '.join(entry['Chest Pain'] for entry in random_values)]

    csv_file_path = "test.csv"
    rows = [row_live, row_beta]

    df= pd.DataFrame(rows, columns=headers)
    if Path(csv_file_path).exists():
        existing_df = pd.read_csv(csv_file_path)
        updated_df = pd.concat([existing_df, df],  ignore_index=True)
        updated_df.to_csv(csv_file_path, index = False)
        # df.to_csv(csv_file_path, index= False)
    else:
        df.to_csv(csv_file_path, index= False)


    status_live_predict = "Right" if status_live == "pass" else "Wrong" if status_live == "fail" else "Wrong"
    status_beta_predict = "Right" if status_beta == "pass" else "Wrong" if status_beta == "fail" else "Wrong"

    print("status_live_predict: ", status_live_predict)
    print('status_beta_predict: ', status_beta_predict)


    # for saving in DB hit new API
    new_url = "https://ekg.pythonanywhere.com/ekg/recordfeedback/"
    payload_live = json.dumps({
        "prescriptions": "-",
        "actual_daignoses": f"{user_key}",
        "predicted_daignoses": f"{', '.join(desease for desease in live_top_diseases)}",
        "correct_status": f"{status_live_predict}",
        "feedback": "this is predict by model",
        "difficult_level": "Easy",
        "prediction_model": "Live"
        })
    
    payload_beta = json.dumps({
        "prescriptions": "-",
        "actual_daignoses": f"{user_key}",
        "predicted_daignoses": f"{', '.join(desease for desease in beta_top_diseases)}",
        "correct_status": f"{status_beta_predict}",
        "feedback": "this is predict by model",
        "difficult_level": "Easy",
        "prediction_model": "Beta"
        })
    
    
    headers = {
    'Content-Type': 'application/json'
    }
    # https://ekg.pythonanywhere.com
    time.sleep(1)
    response_live = requests.request("POST", new_url, headers=headers, data=payload_live, timeout=300)
    # time.sleep(1)
    response_beta = requests.request("POST", new_url, headers=headers, data=payload_beta, timeout=300)

    # print("payload_live: ", payload_live)
    # print("payload_beta: ", payload_beta)

    print("\n\n")

    print("response_live: ",response_live.text)
    print("response_beta: ",response_beta.text)

    print(f"**************** COMPLETE {test_num} COMPLETE ***********************")

    # time.sleep(3)


    

