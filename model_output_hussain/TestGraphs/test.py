import matplotlib.pyplot as plt

data = {
    "status": True,
    "live": {
        "status": True,
        "version": "v2",
        "data": [
            {
                "diseases_name": "Infarct",
                "probability": 0.40418
            },
            {
                "diseases_name": "Pulmonary",
                "probability": 0.383
            },
            {
                "diseases_name": "Ischemia",
                "probability": 0.31491
            },
            {
                "diseases_name": "PE",
                "probability": 0.28718
            },
            {
                "diseases_name": "Pericarditis",
                "probability": 0.22891
            },
            {
                "diseases_name": "CHF",
                "probability": 0.21
            },
            {
                "diseases_name": "Aortic Dissection",
                "probability": 0.15891
            },
            {
                "diseases_name": "AS/AI",
                "probability": 0.11627
            },
            {
                "diseases_name": "GI",
                "probability": 0.11264
            },
            {
                "diseases_name": "MS",
                "probability": 0.03609
            },
            {
                "diseases_name": "Eso rupture",
                "probability": 0.03055
            }
        ],
        "testsuggestion": [
            {
                "test_name": "EKG",
                "probability": 0.6773
            },
            {
                "test_name": "HsTnT 0H",
                "probability": 0.6045
            },
            {
                "test_name": "D-Dimer",
                "probability": 0.5364
            },
            {
                "test_name": "NT pro BNP",
                "probability": 0.3691
            },
            {
                "test_name": "WBC",
                "probability": 0.3691
            },
            {
                "test_name": "CXR",
                "probability": 0.2473
            },
            {
                "test_name": "ESR",
                "probability": 0.2364
            },
            {
                "test_name": "CRP",
                "probability": 0.2364
            },
            {
                "test_name": "Hb",
                "probability": 0.1873
            },
            {
                "test_name": "CT",
                "probability": 0.1164
            },
            {
                "test_name": "ECHO",
                "probability": 0.0718
            },
            {
                "test_name": "No further test",
                "probability": 0.06269999999999999
            }
        ]
    },
    "beta": {
        "status": True,
        "version": "v2",
        "data": [
            {
                "diseases_name": "Infarct",
                "probability": 0.19892553829135895
            },
            {
                "diseases_name": "Ischemia",
                "probability": 0.14116075028931463
            },
            {
                "diseases_name": "Pericarditis",
                "probability": 0.1125153450724794
            },
            {
                "diseases_name": "AS/AI",
                "probability": 0.09424398002778371
            },
            {
                "diseases_name": "Eso rupture",
                "probability": 0.08307977690026973
            },
            {
                "diseases_name": "Pulmonary",
                "probability": 0.08271534983092636
            },
            {
                "diseases_name": "PE",
                "probability": 0.0806605734312323
            },
            {
                "diseases_name": "Aortic Dissection",
                "probability": 0.07434378305816072
            },
            {
                "diseases_name": "CHF",
                "probability": 0.05967939056639239
            },
            {
                "diseases_name": "GI",
                "probability": 0.04635156530160191
            },
            {
                "diseases_name": "MS",
                "probability": 0.026323947230478963
            }
        ],
        "testsuggestion": [
            {
                "test_name": "EKG",
                "probability": 0.617
            },
            {
                "test_name": "HsTnT 0H",
                "probability": 0.366
            },
            {
                "test_name": "CRP",
                "probability": 0.005
            },
            {
                "test_name": "ESR",
                "probability": 0.005
            },
            {
                "test_name": "NT pro BNP",
                "probability": 0.003
            },
            {
                "test_name": "WBC",
                "probability": 0.003
            },
            {
                "test_name": "D-Dimer",
                "probability": 0.002
            },
            {
                "test_name": "CXR",
                "probability": 0.001
            },
            {
                "test_name": "CT",
                "probability": 0
            },
            {
                "test_name": "ECHO",
                "probability": 0
            },
            {
                "test_name": "Hb",
                "probability": 0
            },
            {
                "test_name": "No further test",
                "probability": 0
            }
        ]
    }
}


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


disease_data= data["live"]['data']
test_sugg_data= data['live']['testsuggestion']


create_analysis_symptoms(disease_data, "Pulmonary", "live", "images/1_live_diseaseAnalysis")

create_test_suggestion(test_sugg_data, "Pulmonary", "live" , "images/1_live_testSuggestion")