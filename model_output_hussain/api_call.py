import requests
import json
import random
from pprint import pprint

# Function to get random chest_pain_values and question_values for a given key
def get_random_values(user_key, num_values, result_dict):
    if user_key in result_dict:
        df_list = result_dict[user_key]
        
        # Check if the requested number of values is greater than the available entries
        num_values = min(num_values, len(df_list))
        
        # Randomly select 'num_values' entries
        random_entries = random.sample(df_list, num_values)

        return random_entries
    else:
        return None


# Ask the user for a key
user_key = input("Enter a key from result_dict: ")

# Ask the user for the number of random values to retrieve
num_values = int(input("Enter the number of random values to retrieve: "))

result_dict = json.load(open("dict.json", "r"))

# Get random values for the specified key
random_values = get_random_values(user_key, num_values, result_dict)

# Display the result
if random_values is not None:
    print(f"Random values for key '{user_key}':")
    for i, entry in enumerate(random_values, start=1):
        print(f"{i}. Chest Pain: {entry['Chest Pain']}, Question: {entry['question']}")

    # Prepare the payload for the API request
    api_payload = {
        "all_symtoms": [{"id": entry['question'], "symtoms": entry['Chest Pain']} for entry in random_values],
        "current": [{"id": entry['question'], "symtoms": entry['Chest Pain']} for entry in random_values]
    }

    # Convert the payload to JSON
    api_payload_json = json.dumps(api_payload)

    # API request
    url = "http://192.168.0.122:8006/ekg/both_symtoms_prediction/?action=v1"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=api_payload_json)

    # Print API response
    print("\n\n")
    print(json.dumps(response.json()))
    response_json = response.json()
else:
    print(f"The key '{user_key}' is not found in result_dict.")
