import statsmodels.api as sm
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
import pandas as pd
import matplotlib as plt
pd.set_option('display.max_columns', 100)

# loading the dataset
df = pd.read_csv('Modeling_Data_04142022.csv')

# Incident Models
# split into training and testing data for incident models

df_y_incident = df["incidentTime_1yr"]
df_x_incident = df.drop(['IncidentStatus',"True_Incident","Total_Incidents",'incidentTime_1yr',
                         'inspectTime_1yr','PlaceKey ID','Action Taken: Investigation',
                          'Action Taken: None','Action Taken: Fill-in, Standby','Action Taken: FireControl',
                          'Action Taken: Services','Action Taken: Assistance','Action Taken: Search & Rescue',
                          'Action Taken: Hazardous Condition','Action Taken: EMS and Transport',
                          'Action Taken: Fire Rescues'], axis = 1)

X_train, X_test, y_train, y_test = train_test_split(df_x_incident,
                                                    df_y_incident,
                                                    test_size = 0.3)

# INCIDENT MODEL, Logistic Regression

# building the model and fitting the data
model = LogisticRegression(class_weight="balanced")
clf = model.fit(X_train, y_train)
prediction = model.predict(X_test)
model.predict_proba(X_test)

# coefficients table
coefficients = pd.concat([pd.DataFrame(df_x_incident.columns),pd.DataFrame(np.transpose(clf.coef_))], axis = 1)
print("Logistic Regression Feature Coefficients:")
print(coefficients)
#print(prediction)

from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report, confusion_matrix, fbeta_score

predy = clf.predict(X_test)

# Model evaluation
print('Logistic Regression Accuracy = ', accuracy_score(y_test, predy))
print('Logistic Regression Fb score = ', fbeta_score(y_test, predy, beta=4))
plot_confusion_matrix(clf, X_test, y_test)

# Incident Model, Random Forest

from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier(max_depth=10, random_state=0, class_weight="balanced")
clf.fit(X_train, y_train)
feat_labels = df_x_incident.columns
val_list = clf.feature_importances_
idx_list = np.argsort(val_list)[::-1]
print("Random forest feature importance: ")
for f in range(X_train.shape[1]):
  print("%2d) %-*s %f" % (f+1,30,
  feat_labels[idx_list[f]],
  val_list[idx_list[f]]))

from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report, confusion_matrix, fbeta_score

predy = clf.predict(X_test)

# Model evaluation
print('Random Forest Accuracy = ', accuracy_score(y_test, predy))
print('Random Forest Fb score = ', fbeta_score(y_test, predy, beta=4))
#
plot_confusion_matrix(clf, X_test, y_test)

# Generating Risk Scores
risk_score_matrix_rf_1 = clf.predict_proba(df_x_incident)
# print(risk_score_matrix)
# first column: probability of 0
# second column: probability of 1
print(risk_score_matrix_rf_1[:,1])
risk_list_rf = risk_score_matrix_rf_1[:,1]

risk_list_rf_1 = pd.Series(risk_list_rf)
risk_list_rf_1.plot.hist(grid=True,color='#607c8e')

print("Number of identified at risk properties:", risk_list_rf_1[risk_list_rf_1 > 0.5].count())

df["risk_value"] = risk_list_rf
# df.to_csv(r'/Users/jarrett/Documents/Academics/modellingDataWithRiskScore04192022.csv')

df2 = df[["PlaceKey ID","risk_value"]]
df_big = pd.read_csv('Final_Merge_Data_04142022.csv',low_memory=False)
result1 = pd.merge(df_big, df2, how="outer", on=["PlaceKey ID", "PlaceKey ID"])
result1.to_csv(r'/Users/jarrett/Documents/Academics/Risk_Score_Final_Merge_Data_04192022.csv')





# Secondary random forest model to validate significant features

df_y_incident2 = df["incidentTime_1yr"]
df_x_incident2 = df[["bld_ar","tot_act_ar","land_ar","incidentTime_2yr","incidentTime_3yr","incidentTime_4yr","Total_Inspections","InspectionStatus","tot_appr_val"]]

X_train, X_test, y_train, y_test = train_test_split(df_x_incident2,
                                                    df_y_incident2,
                                                    test_size = 0.3)

clf = RandomForestClassifier(max_depth=10, random_state=0, class_weight="balanced")
clf.fit(X_train, y_train)
feat_labels = df_x_incident2.columns
val_list = clf.feature_importances_
idx_list = np.argsort(val_list)[::-1]
print("Feature Significance in selected features model:")
for f in range(X_train.shape[1]):
  print("%2d) %-*s %f" % (f+1,30,
  feat_labels[idx_list[f]],
  val_list[idx_list[f]]))

from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report, confusion_matrix, fbeta_score

predy = clf.predict(X_test)

print('Random forest with selected features Accuracy = ', accuracy_score(y_test, predy))
print('Random forest with selected features Fb score = ', fbeta_score(y_test, predy, beta=4))
#
plot_confusion_matrix(clf, X_test, y_test)