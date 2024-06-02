"""
Main Live Script For Script of Scopium EKG

https://ekg.pythonanywhere.com/ekg/both_symtoms_prediction/?action=v1


"""
import matplotlib.pyplot as plt
import requests
import json
import random
import time
from pprint import pprint
import pandas as pd
from pathlib import Path

DISEASES = ['Aortic Dissection', 'AS/AI', 'CHF', 'Eso rupture', 'GI', 'Infarct', 'Ischemia', 'MS', 'PE', 'Pericarditis', 'Pulmonary']
BASE_URL= "http://127.0.0.1:9001"
# BASE_URL= "https://ekg.pythonanywhere.com/"
THRESHOLD_PROBABILITY = 0.5
NUM_TEST_CASES = 500

def create_analysis_symptoms(data, random_disease, version, save_path):

    # Extract diseases names and probabilities
    diseases = [entry["diseases_name"] for entry in data]
    probabilities = [entry["probability"] for entry in data]

    # Create a vertical bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(diseases, probabilities, color='skyblue')

    # Customize the chart
    plt.title(f'Probability of Diseases {random_disease} on {version}')
    plt.xlabel('Disease')
    plt.ylabel('Probability')
    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
    plt.tight_layout()

    # Save the chart as an image
    if save_path:
        plt.savefig(save_path)
        print(f"Chart saved successfully at {save_path}")

    
    return save_path




def create_test_suggestion(data, random_disease, version, save_path):

    # Extract test names and probabilities
    test_name = [entry["test_name"] for entry in data]
    probabilities = [entry["probability"] for entry in data]

    # Zip test names and probabilities, then sort by probabilities in ascending order
    sorted_data = sorted(zip(test_name, probabilities), key=lambda x: x[1])

    # Extract sorted test names and probabilities
    test_name_sorted = [entry[0] for entry in sorted_data]
    probabilities_sorted = [entry[1] for entry in sorted_data]

    # Create a horizontal bar chart
    plt.figure(figsize=(10, 6))
    plt.barh(test_name_sorted, probabilities_sorted, color='skyblue')  # Use plt.barh() for horizontal bars

    # Customize the chart
    plt.title(f'Test Suggestion of {random_disease} on {version}')
    plt.xlabel('Probability')
    plt.ylabel('Test Name')
    plt.tight_layout()

    # Save the chart as an image
    if save_path:
        plt.savefig(save_path)
        print(f"Chart saved successfully at {save_path}")

    return save_path

def get_symptoms(diseases_name: str, version: str):
    version_data = {
        'v1': 4,
        'v2': 1,
        'v3': 2,
        'v4': 4 
    }
    
    if version in version_data:
        slice_value = version_data[version]
        url = f"{BASE_URL}/ekg/scripting/?disease_name={diseases_name}&version={version}"

        response = requests.request("GET", url)
        resp_data = json.loads(response.text)
        data = resp_data['data']
        print(len(data))

        # Separating age-related symptoms and non-age-related symptoms
        age_symptoms = [symptom for symptom in data if 'Age' in symptom['name']]
        other_symptoms = [symptom for symptom in data if 'Age' not in symptom['name'] and symptom['probability'] >= THRESHOLD_PROBABILITY]
        # Randomly selecting one age-related symptom if available
        # if age key available in resp
        if age_symptoms:
            # check the len of other_symptoms which probability is greater than 0.6, then slice with THRESHOLD
            if len(other_symptoms) >= slice_value -1 :
                selected_symptoms = random.sample(age_symptoms, 1) + random.sample(other_symptoms, slice_value - 1)
            else:
                # if probability is less than 0.6 then slect strats (slice_value) without threshold
                other_symptoms = [symptom for symptom in data if 'Age' not in symptom['name']]
                selected_symptoms = random.sample(age_symptoms, 1) + other_symptoms[:slice_value - 1]
        else:
            if len(other_symptoms) >= slice_value :
                selected_symptoms = random.sample(other_symptoms, slice_value)
            else:
                other_symptoms = [symptom for symptom in data if 'Age' not in symptom['name']]
                selected_symptoms = other_symptoms[:slice_value]
                
        print(len(selected_symptoms))

        if len(selected_symptoms) == 0:
            print(url)
            print(resp_data)

        return selected_symptoms
    else:
        print(f"Problem in {version}  only {version_data} is accepted ....")




for test_num in range(1, NUM_TEST_CASES + 1):
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

        # print(json.dumps(api_payload))
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

        # print("\n\n response_json _________________ \n", json.dumps(response_json, indent=2))

        data = response_json

        live_disease_data= data["live"]['data']
        live_test_sugg_data= data['live']['testsuggestion']

        beta_disease_data= data["beta"]['data']
        beta_test_sugg_data= data['beta']['testsuggestion']

        live_analysis_img_path= create_analysis_symptoms(live_disease_data, random_disease, "live", f"images/{test_num}_LIVE_AnalysisSypmtoms")
        live_test_sugg_img_path =create_test_suggestion(live_test_sugg_data, random_disease, "live" , f"images/{test_num}_LIVE_testSuggestion")

        beta_analysis_img_path= create_analysis_symptoms(beta_disease_data, random_disease, "beta", f"images/{test_num}_BETA_AnalysisSypmtoms")
        beta_test_sugg_img_path =create_test_suggestion(beta_test_sugg_data, random_disease, "beta" , f"images/{test_num}_BETA_testSuggestion")

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

        headers = ["live/beta", "desease", "status", "model_output", "Analysis Symptoms", "Test Suggestion", "symptoms"]
        row_live = ["live", random_disease, status_live, ', '.join(desease for desease in live_top_diseases), live_analysis_img_path, live_test_sugg_img_path , ', '.join(entry['name'] for entry in all_symptoms)]
        row_beta = ["beta", random_disease, status_beta, ', '.join(desease for desease in beta_top_diseases), beta_analysis_img_path, beta_test_sugg_img_path ,', '.join(entry['name'] for entry in all_symptoms)]

        csv_file_path = "testcsvs/random_symptoms_test.csv"
        rows = [row_live, row_beta]

        df= pd.DataFrame(rows, columns=headers)
        if Path(csv_file_path).exists():
            existing_df = pd.read_csv(csv_file_path)
            updated_df = pd.concat([existing_df, df],  ignore_index=True)
            updated_df.to_csv(csv_file_path, index = False)
            # df.to_csv(csv_file_path, index= False)
        else:
            df.to_csv(csv_file_path, index= False)


    #     status_live_predict = "Right" if status_live == "pass" else "Wrong" if status_live == "fail" else "Wrong"
    #     status_beta_predict = "Right" if status_beta == "pass" else "Wrong" if status_beta == "fail" else "Wrong"

    #     print("status_live_predict: ", status_live_predict)
    #     print('status_beta_predict: ', status_beta_predict)


    #     # for saving FEEDBACK in DB hit new API
    #     new_url = f"{BASE_URL}/ekg/recordfeedback/"
    #     payload_live = json.dumps({
    #         "prescriptions": "-",
    #         "actual_daignoses": f"{random_disease}",
    #         "predicted_daignoses": f"{', '.join(desease for desease in live_top_diseases)}",
    #         "correct_status": f"{status_live_predict}",
    #         "feedback": "this is predict by model",
    #         "difficult_level": "Easy",
    #         "prediction_model": "Live"
    #         })
        
    #     payload_beta = json.dumps({
    #         "prescriptions": "-",
    #         "actual_daignoses": f"{random_disease}",
    #         "predicted_daignoses": f"{', '.join(desease for desease in beta_top_diseases)}",
    #         "correct_status": f"{status_beta_predict}",
    #         "feedback": "this is predict by model",
    #         "difficult_level": "Easy",
    #         "prediction_model": "Beta"
    #         })
        
        
    #     headers = {
    #     'Content-Type': 'application/json'
    #     }
    #     time.sleep(1)
    #     response_live = requests.request("POST", new_url, headers=headers, data=payload_live, timeout=300)
    #     # time.sleep(1)
    #     response_beta = requests.request("POST", new_url, headers=headers, data=payload_beta, timeout=300)

    #     print("\n\n")

    #     print("response_live: ",response_live.text)
    #     print("response_beta: ",response_beta.text)

    #     print(f"**************** COMPLETE {test_num} COMPLETE ***********************")

    # else:
    #     print("Length is not equal to 11 ")
    #     break


    

