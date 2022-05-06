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
df = pd.read_csv('Modeling Data')

# INSPECTION MODEL

# Logistic Regression Model
# split into training and testing data
df_y_inspection = df["inspectTime_1yr"]
df_x_inspection = df.drop(['InspectionStatus',"Total_Inspections",'inspectTime_1yr',
                           'incidentTime_1yr','PlaceKey ID'], axis = 1)

X_train, X_test, y_train, y_test = train_test_split(df_x_inspection,
                                                    df_y_inspection,
                                                    test_size = 0.3)

# building the model and fitting the data
model = LogisticRegression(class_weight="balanced")
clf = model.fit(X_train, y_train)
prediction = model.predict(X_test)
#print(prediction)

# coefficients table
coefficients = pd.concat([pd.DataFrame(df_x_inspection.columns),pd.DataFrame(np.transpose(clf.coef_))], axis = 1)
print("Logistic Regression Feature Coefficients:")
print(coefficients)
#print(prediction)

from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report, confusion_matrix, fbeta_score

predy = clf.predict(X_test)

# Model evaluation
print('Logistic Regression Accuracy = ', accuracy_score(y_test, predy))
print('Logistic Regression Fb score = ', fbeta_score(y_test, predy, beta=4))
plot_confusion_matrix(clf, X_test, y_test)


# Random Forest Model
clf = RandomForestClassifier(max_depth=10, random_state=0, class_weight="balanced")
clf.fit(X_train, y_train)
feat_labels = df_x_inspection.columns
val_list = clf.feature_importances_
idx_list = np.argsort(val_list)[::-1]
print("Random forest feature importance: ")
for f in range(X_train.shape[1]):
  print("%2d) %-*s %f" % (f+1,30,
  feat_labels[idx_list[f]],
  val_list[idx_list[f]]))

#

from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report, confusion_matrix, fbeta_score

predy = clf.predict(X_test)

# Model evaluation
print('Random Forest Accuracy = ', accuracy_score(y_test, predy))
print('Random Forest Fb score = ', fbeta_score(y_test, predy, beta=4))

plot_confusion_matrix(clf, X_test, y_test)


# Secondary random forest model to validate significant features

# split into training and testing data
df_y_inspection2 = df["inspectTime_1yr"]
df_x_inspection2 = df[['bld_ar','tot_act_ar','land_ar',"inspectTime_2yr",'inspectTime_5yr','Total_Incidents','True_Incident','IncidentStatus','Total_Violations','tot_appr_val']]

X_train, X_test, y_train, y_test = train_test_split(df_x_inspection2,
                                                    df_y_inspection2,
                                                    test_size = 0.3)

clf = RandomForestClassifier(max_depth=10, random_state=0, class_weight="balanced")
clf.fit(X_train, y_train)
feat_labels = df_x_inspection2.columns
val_list = clf.feature_importances_
idx_list = np.argsort(val_list)[::-1]
print("Feature Significance in selected features model:")
for f in range(X_train.shape[1]):
  print("%2d) %-*s %f" % (f+1,30,
  feat_labels[idx_list[f]],
  val_list[idx_list[f]]))


from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report, confusion_matrix, fbeta_score

predy = clf.predict(X_test)

# Model evaluation
print('Random forest with selected features Accuracy = ', accuracy_score(y_test, predy))
print('Random forest with selected features Fb score = ', fbeta_score(y_test, predy, beta=4))
plot_confusion_matrix(clf, X_test, y_test)
