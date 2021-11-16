import pandas as pd # for data manipulation
import networkx as nx # for drawing graphs
import matplotlib.pyplot as plt # for drawing graphs

def getcode(p):
    if p[0:3].isnumeric():
        return int(p[0:3])
    return 0

def prop_cat(propcode):
    code = getcode(propcode)
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
    code = getcode(incidcode)
    if code >= 100 and code <= 500:
        return "Yes"
    return "No"

def incid_cat(incidcode):
    code = getcode(incidcode)
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

pd.options.display.max_columns = 15
df = pd.read_csv('../data/IncidentData.csv')
df = df[pd.isnull(df['PropCode']) == False]
df = df[pd.isnull(df['IncidentCode']) == False]

# Create bands for variables that we want to use in the model
df['PropCode'] = df['PropCode'].apply(lambda x: prop_cat(x))
df['IncidentCode'] = df['IncidentCode'].apply(lambda x: incid_exist(x))

print(df.head(20))