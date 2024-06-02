import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import pandas as pd

DISEASES = ['Aortic Dissection', 'AS/AI', 'CHF', 'Eso rupture', 'GI', 'Infarct', 'Ischemia', 'MS', 'PE', 'Pericarditis', 'Pulmonary']


# file_path = 'test.csv'
file_path = 'testcsvs/random_symptoms_test.csv'
# file_path = 'testcsvs/highest_probab_test.csv'
df = pd.read_csv(file_path)

# separate live and beta
live_data = df[df['live/beta'] == 'live']
beta_data = df[df['live/beta'] == 'beta']


# all live actual and model_predict data
live_actual_predict = live_data['desease']
live_model_predict = live_data['model_output'].str.split(',')

# filter live pass and fail data because both will integrate diff logic
live_fail_data = df[(df['live/beta'] == 'live') & (df['status'] == 'fail')]
live_pass_data = df[(df['live/beta'] == 'live') & (df['status'] == 'pass')]

# On Live Fail, separate actual and model_predict data 
# In model_output it has 2 disease in list, so pick the first 
live_fail_actual_predict = live_fail_data['desease'].tolist()
live_fail_model_predict = live_fail_data['model_output'].str.split(',').str[0].tolist()

# On Live Pass, separate actual and model_predict data 
live_pass_actual_predict = live_pass_data['desease'].tolist()
live_pass_model_predict = live_pass_actual_predict


# mix both Pass and Fail    data of    actual and model_predict
live_actual_data = live_fail_actual_predict + live_pass_actual_predict
live_model_predict_data = live_fail_model_predict + live_pass_model_predict

# Create the confusion matrix
cm = confusion_matrix(live_actual_data, live_model_predict_data)

# Get unique labels from the actual predictions
labels = sorted(set(live_actual_data + live_model_predict_data))

# Convert confusion matrix to DataFrame for better visualization
cm_df = pd.DataFrame(cm, index=labels, columns=labels)

# Plot confusion matrix
plt.figure(figsize=(10, 7))
sns.heatmap(cm_df, annot=True, cmap='Blues', fmt='d')  # Use 'd' format to display integer counts
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('LIVE Confusion Matrix')
plt.show()





beta_data = df[df['live/beta'] == 'beta']

# all beta actual and model_predict data
beta_actual_predict = beta_data['desease']
beta_model_predict = beta_data['model_output'].str.split(',')

# filter beta pass and fail data because both will integrate diff logic
beta_fail_data = df[(df['live/beta'] == 'beta') & (df['status'] == 'fail')]
beta_pass_data = df[(df['live/beta'] == 'beta') & (df['status'] == 'pass')]

# On beta Fail, separate actual and model_predict data 
# In model_output it has 2 disease in list, so pick the first 
beta_fail_actual_predict = beta_fail_data['desease'].tolist()
beta_fail_model_predict = beta_fail_data['model_output'].str.split(',').str[0].tolist()

# On beta Pass, separate actual and model_predict data 
beta_pass_actual_predict = beta_pass_data['desease'].tolist()
beta_pass_model_predict = beta_pass_actual_predict


# mix both Pass and Fail    data of    actual and model_predict
beta_actual_data = beta_fail_actual_predict + beta_pass_actual_predict
beta_model_predict_data = beta_fail_model_predict + beta_pass_model_predict

# Create the confusion matrix
cm = confusion_matrix(beta_actual_data, beta_model_predict_data)

# Get unique labels from the actual predictions
labels = sorted(set(beta_actual_data + beta_model_predict_data))

# Convert confusion matrix to DataFrame for better visualization
cm_df = pd.DataFrame(cm, index=labels, columns=labels)

# Plot confusion matrix
plt.figure(figsize=(10, 7))
sns.heatmap(cm_df, annot=True, cmap='Blues', fmt='d')  # Use 'd' format to display integer counts
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('BETA Confusion Matrix')
plt.show()
