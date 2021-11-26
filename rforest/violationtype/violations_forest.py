import pandas as pd # for data manipulation
import collections
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import model_selection
import networkx as nx # for drawing graphs
import matplotlib.pyplot as plt # for drawing graphs

# random forest parameters
# inputs: ZIP, TEAMCODE, APTYPE, STNAME?, INSPTYPECAT?
# output: VIOLATIONCode

# global map and id counter for the Team types
team_map = collections.defaultdict(int)
team_id = 1

# global map and id counter for the AP types
ap_map = collections.defaultdict(int)
ap_id = 1

# global map and id counter for the violation codes
viol_map = collections.defaultdict(int)
viol_id = 1

# Helper functions to convert/process column data to int
# data types through mappings
def get_zip(addr):
    return int(addr)

def proc_teamcode(team):
    global team_map
    global team_id
    if team_map[team] == 0:
        team_map[team] = team_id
        team_id += 1
    return int(team_map[team])

def proc_apcode(ap):
    global ap_map
    global ap_id
    if ap_map[ap] == 0:
        ap_map[ap] = ap_id
        ap_id += 1
    return int(ap_map[ap_id])

def proc_violation(viol):
    global viol_map
    global viol_id
    if viol_map[viol] == 0:
        viol_map[viol] = viol_id
        viol_id += 1
    return int(viol_map[viol_id])

# pd.options.display.max_columns = 15
df = pd.read_csv('../../data/2020_2021_Violation_Recs.csv')

# Dropping non-essential columns and removing rows with no data
df = df[['ZIP','TEAMCODE', 'APTYPE', 'VIOLATIONCode']]
df = df[pd.isnull(df['ZIP']) == False]
df = df[pd.isnull(df['TEAMCODE']) == False]
df = df[pd.isnull(df['APTYPE']) == False]
df = df[pd.isnull(df['VIOLATIONCode']) == False]

# Create bands for variables that we want to use in the model
df['ZIP'] = df['ZIP'].apply(lambda x: get_zip(x))
df['TEAMCODE'] = df['TEAMCODE'].apply(lambda x: proc_teamcode(x))
df['APTYPE'] = df['APTYPE'].apply(lambda x: proc_apcode(x))
df['VIOLATIONCode'] = df['VIOLATIONCode'].apply(lambda x: proc_violation(x))

# Print check
print(df.head(20))

# Set all columns but the incident code in dataframe as inputs,
# set incident code as output
x = df.drop('VIOLATIONCode', axis=1)
y = df['VIOLATIONCode']

# Split data into training and testing data, and train forest on training data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.33, random_state=66)
rfc = RandomForestClassifier()
rfc.fit(x_train, y_train)

# Run tests on generated random forest model
rfc_predict = rfc.predict(x_test)
rfc_cv_score = cross_val_score(rfc, x, y, cv=10, scoring='roc_auc')

print("=== Confusion Matrix ===")
print(confusion_matrix(y_test, rfc_predict))
print('\n')
print("=== Classification Report ===")
print(classification_report(y_test, rfc_predict))
print('\n')
print("=== All AUC Scores ===")
print(rfc_cv_score)
print('\n')
print("=== Mean AUC Score ===")
print("Mean AUC Score - Random Forest: ", rfc_cv_score.mean())

