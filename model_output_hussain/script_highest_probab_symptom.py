"""
Main Live Script For Script of Scopium EKG

https://ekg.pythonanywhere.com/ekg/both_symtoms_prediction/?action=v1

Running Testcases and see on the live and cross-check the tests 


# Number of test cases
num_tests = 1500

Select Highest Probability Symptoms from the API

"""

import requests
import json
import random
import time
from pprint import pprint
import pandas as pd
from pathlib import Path

DISEASES = ['Aortic Dissection', 'AS/AI', 'CHF', 'Eso rupture', 'GI', 'Infarct', 'Ischemia', 'MS', 'PE', 'Pericarditis', 'Pulmonary']
BASE_URL= "http://127.0.0.1:8000"


def get_symptoms(diseases_name: str, version: str):
    version_data = {
        'v1': 4,
        'v2': 1,
        'v3': 2,
        'v4': 4 
    }
    
    slice_value = version_data.get(version, None)
    
    if slice_value is not None:
        url = f"{BASE_URL}/ekg/scripting/?disease_name={diseases_name}&version={version}"

        response = requests.request("GET", url)
        resp_data = json.loads(response.text)
        data = resp_data['data']
        print(len(data))
        
        # Separating age-related symptoms and non-age-related symptoms
        age_symptoms = [symptom for symptom in data if 'Age' in symptom['name']]
        other_symptoms = [symptom for symptom in data if 'Age' not in symptom['name']]

        selected_age_symptom = age_symptoms[0] if age_symptoms else None
        
        if selected_age_symptom:
            selected_symptoms = [selected_age_symptom] + other_symptoms[: slice_value - 1]
        else:
            selected_symptoms = data[:slice_value]

        print(len(selected_symptoms))

        if len(selected_symptoms) == 0:
            print(url)
            print(resp_data)

        return selected_symptoms
    else:
        print(f"Problem in {version}  only {version_data} is accepted ....")







# Number of test cases
num_tests = 2000

for test_num in range(1, num_tests + 1):
    # time.sleep(1)

    print(f"\n\n**************** START {test_num} ***********************")

    random_disease = random.choice(DISEASES)
    print("Input: ",random_disease)

    # all symptoms from all version v1 to v4
    all_symptoms = []

    versions= ["v1", "v2", "v3", "v4"]
    
    for version in versions:
        print(f"\n\n\t********* START {version} *********")
        # time.sleep(1)
        symptoms = get_symptoms(diseases_name= random_disease, version= version)
        all_symptoms.extend(symptoms)

    print("all_symptoms LENGTH ",len(all_symptoms))

    if len(all_symptoms) == 11:

        # Make a payload for sending a data to the API for run test cases
        api_payload = {
            "all_symtoms": [{"id": entry['question_id'], "symtoms": entry['name']} for entry in all_symptoms],
            "current": [{"id": entry['question_id'], "symtoms": entry['name']} for entry in all_symptoms]
        }

        print(json.dumps(api_payload))
        # Convert the payload to JSON
        api_payload_json = json.dumps(api_payload)

        url = f"{BASE_URL}/ekg/both_symtoms_prediction/?action=v1"
        headers = {'Content-Type': 'application/json'}
        # time.sleep(1)
        response = requests.post(url, headers=headers, data=api_payload_json, timeout=300)
        # time.sleep(2)
        
        response_json = response.json()
        try:
            live_data = response_json["live"]["data"]
            beta_data = response_json["beta"]["data"]
        except KeyError:
            print("\n\n **************************************************************************************")
            print("\n\nERROR API and Payload  !!!!!!!!!!!!!!!")
            print("\nResponse")
            print(json.dumps(response_json))
            print("\n\n **************************************************************************************")
            break

        live_top_diseases = [entry['diseases_name'] for entry in live_data[:2]]
        beta_top_diseases = [entry['diseases_name'] for entry in beta_data[:2]]

        print("live_top_diseases: ",live_top_diseases)
        print("beta_top_diseases: ", beta_top_diseases)

        # For matching must convert to lowercase
        disease_lower = random_disease.lower()
        live_top_diseases_lower = [desease.lower() for desease in live_top_diseases]
        beta_top_diseases_lower = [desease.lower() for desease in beta_top_diseases]

        status_live = "pass" if disease_lower in live_top_diseases_lower else "fail"
        status_beta = "pass" if disease_lower in beta_top_diseases_lower else "fail"

        print("Input: ",random_disease)
        print("status_live: ", status_live)
        print('status_beta: ', status_beta)

        headers = ["live/beta", "desease", "status", "model_output", "symptoms"]
        row_live = ["live", random_disease, status_live, ', '.join(desease for desease in live_top_diseases),  ', '.join(entry['name'] for entry in all_symptoms)]
        row_beta = ["beta", random_disease, status_beta, ', '.join(desease for desease in beta_top_diseases),  ', '.join(entry['name'] for entry in all_symptoms)]

        csv_file_path = "testcsvs/highest_probab_test.csv"
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


        # for saving FEEDBACK in DB hit new API
        new_url = f"{BASE_URL}/ekg/recordfeedback/"
        payload_live = json.dumps({
            "prescriptions": "-",
            "actual_daignoses": f"{random_disease}",
            "predicted_daignoses": f"{', '.join(desease for desease in live_top_diseases)}",
            "correct_status": f"{status_live_predict}",
            "feedback": "this is predict by model",
            "difficult_level": "Easy",
            "prediction_model": "Live"
            })
        
        payload_beta = json.dumps({
            "prescriptions": "-",
            "actual_daignoses": f"{random_disease}",
            "predicted_daignoses": f"{', '.join(desease for desease in beta_top_diseases)}",
            "correct_status": f"{status_beta_predict}",
            "feedback": "this is predict by model",
            "difficult_level": "Easy",
            "prediction_model": "Beta"
            })
        
        
        headers = {
        'Content-Type': 'application/json'
        }
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

    else:
        print("Length is not equal to 11 ")
        break


    

