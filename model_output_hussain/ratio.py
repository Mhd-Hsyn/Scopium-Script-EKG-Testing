"""
This script read the test.csv  where all test-cases data which are run through script.py
after reading test.csv it create a ratio.csv where all symptoms ratio are save 
 
"""


import csv, json
from collections import Counter

def filter_and_calculate_percentage(input_file):
    # Initialize counters
    live_pass_count = 0
    live_fail_count = 0
    beta_pass_count = 0
    beta_fail_count = 0
    total_live = 0
    total_beta = 0

    live_failed_diseases, beta_failed_diseases = [], []
    live_pass_disease, beta_pass_disease= [], []
    live_total_disease , beta_total_disease = [], []

    # Open CSV file and iterate through rows
    with open(f"{input_file}.csv", 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['live/beta'] == 'live':
                total_live += 1
                live_total_disease.append(row["desease"])
                if row['status'] == 'pass':
                    live_pass_count += 1
                    live_pass_disease.append(row["desease"])
                elif row['status'] == 'fail':
                    live_fail_count += 1
                    live_failed_diseases.append(row['desease'])


            elif row['live/beta'] == 'beta':
                total_beta += 1
                beta_total_disease.append(row["desease"])
                if row['status'] == 'pass':
                    beta_pass_count += 1
                    beta_pass_disease.append(row['desease'])
                elif row['status'] == 'fail':
                    beta_fail_count += 1
                    beta_failed_diseases.append(row['desease'])

    # Calculate percentages
    live_pass_percentage = (live_pass_count / total_live) * 100 if total_live > 0 else 0
    live_fail_percentage = (live_fail_count / total_live) * 100 if total_live > 0 else 0
    beta_pass_percentage = (beta_pass_count / total_beta) * 100 if total_beta > 0 else 0
    beta_fail_percentage = (beta_fail_count / total_beta) * 100 if total_beta > 0 else 0



    # Format percentages with two digits after the decimal point
    live_pass_percentage = "{:.2f}".format(live_pass_percentage)
    live_fail_percentage = "{:.2f}".format(live_fail_percentage)
    beta_pass_percentage = "{:.2f}".format(beta_pass_percentage)
    beta_fail_percentage = "{:.2f}".format(beta_fail_percentage)


     # Print results
    print("\n")
    print("ALL TEST COUNT: ", total_live+total_beta)
    
    print("\nLIVE TEST COUNT: ", total_live)
    print("BETA TEST COUNT: ", total_beta)

    print("\nLive - live_pass_count :", live_pass_count)
    print("Live - live_fail_count :", live_fail_count)
    print("beta - beta_pass_count :", beta_pass_count)
    print("beta - beta_fail_count :", beta_fail_count)


    print("\nLive - Pass Percentage:", live_pass_percentage, "%")
    print("Live - Fail Percentage:", live_fail_percentage, "%")
    print("Beta - Pass Percentage:", beta_pass_percentage, "%")
    print("Beta - Fail Percentage:", beta_fail_percentage, "%")

    print("\n")

    # Total Count 
    live_total_disease_count = dict(Counter(live_total_disease))
    beta_total_disease_count = dict(Counter(beta_total_disease))
    print(json.dumps(live_total_disease_count    , indent=2))
    print(json.dumps(beta_total_disease_count    , indent=2))
   
    # PASS Count occurrences of diseases
    live_pass_disease_count = dict(Counter(live_pass_disease))
    beta_pass_disease_count = dict(Counter(beta_pass_disease))
    print(json.dumps(live_pass_disease_count    , indent=2))
    print(json.dumps(beta_pass_disease_count    , indent=2))


    # FAIL Count occurrences of diseases
    live_failed_disease_count = dict(Counter(live_failed_diseases))
    beta_failed_disease_count = dict(Counter(beta_failed_diseases))


    # print("\nLIVE Failed disease names and their fail counts:\n")
    print(json.dumps(live_failed_disease_count, indent=2))

    # for disease , count in live_failed_disease_count.items():
    #     print(f"{disease} : {count} ")



    # print("\n\nBETA Failed disease names and their fail counts:\n")
    print(json.dumps(beta_failed_disease_count, indent=2))

    # for disease, count in beta_failed_disease_count.items():
    #     print(f"{disease} : {count} ")


    # Write data to CSV file
    with open(f'{input_file}_ratio.csv', 'w', newline='') as csvfile:
        fieldnames = ['Disease', 'Live Total Count', 'Beta Total Count', 'Live Pass Count', 'Beta Pass Count', 'Live Fail Count', 'Beta Fail Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for disease in live_total_disease_count:
            writer.writerow({
                'Disease': disease,
                'Live Total Count': live_total_disease_count.get(disease, 0),
                'Beta Total Count': beta_total_disease_count.get(disease, 0),
                'Live Pass Count': live_pass_disease_count.get(disease, 0),
                'Beta Pass Count': beta_pass_disease_count.get(disease, 0),
                'Live Fail Count': live_failed_disease_count.get(disease, 0),
                'Beta Fail Count': beta_failed_disease_count.get(disease, 0)
            })



# Example usage:
# input_file = 'test'
            

# input_file = 'testcsvs/highest_probab_test'
input_file = 'testcsvs/random_symptoms_test'


filter_and_calculate_percentage(input_file)
