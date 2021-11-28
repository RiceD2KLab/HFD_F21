import pandas as pd # for data manipulation
import collections
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import model_selection
import networkx as nx # for drawing graphs
import matplotlib.pyplot as plt # for drawing graphs

# list for likely incidents
inc_predict = []

# global map and counter for the EFD card number IDs
card_map = collections.defaultdict(list)
card_id = 1

# build card map dictionary
efd = pd.read_excel('../../data/CardNumber.xlsx')

for ind, row in efd.iterrows():
    # global card_map
    # global card_id
    card = row["TYPE"]
    if len(card) < 5:
        if card_map[card] == []:
            card_map[card].append(card_id)
            card_map[card].append(row["DESCR"])
    else:
        if card_map[card[0:5]] == []:
            card_map[card[0:5]].append(card_id)
            card_map[card[0:5]].append(row["DESCR"])
    card_id += 1

# Helper functions to convert/process column data to int
# data types and categories
def get_code(p):
    if p[0:3].isnumeric():
        return int(p[0:3])
    return 0

def get_zip(addr):
    return int(addr[-5:])

def prop_num(propcode):
    code = get_code(propcode)
    if code >= 100 and code < 200:
        return 100
    elif code >= 200 and code < 300:
        return 200
    elif code >= 300 and code < 400:
        return 300
    elif code >= 400 and code < 500:
        return 400
    elif code >= 500 and code < 600:
        return 500
    elif code >= 600 and code < 700:
        return 600
    elif code >= 700 and code < 800:
        return 700
    elif code >= 800 and code < 900:
        return 800
    elif code >= 900 and code < 1000:
        return 900
    elif code == 000:
        return 000
    return -1

def prop_cat(propcode):
    code = get_code(propcode)
    if code >= 100 and code < 200:
        return "Assembly"
    elif code >= 200 and code < 300:
        return "Educational"
    elif code >= 300 and code < 400:
        return "HCDC"
    elif code >= 400 and code < 500:
        return "Residential"
    elif code >= 500 and code < 600:
        return "Mercantile"
    elif code >= 600 and code < 700:
        return "Industrial"
    elif code >= 700 and code < 800:
        return "Manufacturing"
    elif code >= 800 and code < 900:
        return "Storage"
    elif code >= 900 and code < 1000:
        return "Special"
    elif code == 000:
        return "Other"
    return "None"

def incid_exist(incidcode):
    code = get_code(incidcode)
    if code >= 100 and code <= 500:
        return 1
    return 0

def incid_cat(incidcode):
    code = get_code(incidcode)
    if code >= 100 and code < 200:
        return "Fire"
    elif code >= 200 and code < 300:
        return "Rupture"
    elif code >= 300 and code < 400:
        return "Rescue"
    elif code >= 400 and code < 500:
        return "Hazardous"
    elif code >= 500 and code < 600:
        return "Service"
    elif code >= 600 and code < 700:
        return "Good Intent"
    elif code >= 700 and code < 800:
        return "False Alarm"
    elif code >= 800 and code < 900:
        return "Natural Disaster"
    elif code >= 900 and code < 1000:
        return "Special"
    elif code == 000:
        return "Other"
    return "None"

def proc_cardnum(card):
    global card_map
    if len(card) < 5:
        # print(card_map[card][0])
        if card in card_map:
            return int(card_map[card][0])
        return 0
    if card[0:5] in card_map:
        return int(card_map[card[0:5]][0])
    return 0

pd.options.display.max_columns = 15
df = pd.read_csv('../../data/IncidentData.csv', low_memory=False)

# Dropping non-essential columns and removing rows with no data
df = df.drop(columns=['Basic Incident Number (FD1)', 'Basic Incident Full Street Address',
                 'Basic Apparatus Call Sign List',
                 'Basic Incident Date Time', 'Basic Property Pre-Incident Value (FD1.37)',
                 'Basic Property Losses (FD1.35)', 'ActionCode'])
df = df[pd.isnull(df['PropCode']) == False]
df = df[pd.isnull(df['IncidentCode']) == False]
df = df[pd.isnull(df['Basic Incident Full Address']) == False]
df = df[pd.isnull(df['Basic EFD Card Number (FD1.84)']) == False]

# Create bands for variables that we want to use in the model
df['PropCode'] = df['PropCode'].apply(lambda x: prop_num(x))
df['IncidentCode'] = df['IncidentCode'].apply(lambda x: incid_exist(x))
zip_col = df['Basic Incident Full Address'].apply(lambda x: get_zip(x))
card_col = df['Basic EFD Card Number (FD1.84)'].apply(lambda x: proc_cardnum(x))

# Remove columns with original labels and replace with simpler labels
df = df.drop(columns=['Basic Incident Full Address'])
df = df.drop(columns=['Basic EFD Card Number (FD1.84)'])
df.insert(0, 'Zip', zip_col)
df.insert(0, 'CardNum', card_col)

# Print check
# print(df.head(20))

# Set all columns but the incident code in dataframe as inputs,
# set incident code as output
x = df.drop('IncidentCode', axis=1)
y = df['IncidentCode']

# Split data into training and testing data, and train forest on training data
# Accuracy will improve if whole dataset used for training
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.33, random_state=66)
rfc = RandomForestClassifier()
rfc.fit(x_train.values, y_train.values)

# Run tests on generated random forest model
# rfc_predict = rfc.predict(x_test)
# rfc_cv_score = cross_val_score(rfc, x, y, cv=10, scoring='roc_auc')
#
# print("=== Confusion Matrix ===")
# print(confusion_matrix(y_test, rfc_predict))
# print('\n')
# print("=== Classification Report ===")
# print(classification_report(y_test, rfc_predict))
# print('\n')
# print("=== All AUC Scores ===")
# print(rfc_cv_score)
# print('\n')
# print("=== Mean AUC Score ===")
# print("Mean AUC Score - Random Forest: ", rfc_cv_score.mean())
#

def predictTop5(zip, propcode):
    # Build list of likely incidents (card nums)
    print("Zipcode: " + str(zip), "Propcode: " + str(propcode))
    print("")
    for key in card_map.keys():
       p_val = rfc.predict_proba([[card_map[key][0], zip, propcode]])[:,1]
       inc_predict.append((p_val, key))

    # Sort by greatest to least and print top 5
    inc_predict.sort(reverse = True, key = lambda x: x[0])
    # print(inc_predict[0:5])

    print("probability", "incident desc.")
    for card in inc_predict[0:5]:
        print(card[0][0], card_map[card[1]][1])

## Test Case Example
predictTop5(77494, 000)