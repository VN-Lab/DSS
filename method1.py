# -*- coding: utf-8 -*-
"""method1

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1s3O4y9wJmIX_hs60EGqJH4r4ILHeVJtC
"""

import numpy as np # linear algebra
import pandas as pd 
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import f1_score, roc_auc_score, roc_curve
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
data = pd.read_csv('DSS2.csv')
data['SIFT'].fillna(value = 'tolerated',inplace =True)



"""### SELECTING FEATURE and Data Preprocessing



*   **AS_SB_TABLE** Forward and reverse read counts for each allele, with alleles separated by the pipe character
• **DP** Approximate read depth
• **GERMQ**The phred-scaled posterior probability that the alternate allele(s) are not germline variants
**MBQ**Median base quality of each allele
*  **MMQ**Median mapping quality of each allele
• **MPOS** Median distance from the end of the read for each alternate allele
• **TLOD**Log odds that the variant is present in the tumor sample relative to the expected noise
•**POPAF** Population allele frequency of the alternate alleles
"""

x = data[['VARIANT_CLASS','TLOD','shiftscore', 'Sample.AF', 'SIFT','MBQ', 'MFRL', 'MMQ','Sample.AD', 'Sample.F1R2', 'Sample.F2R1', 'DP', 'GERMQ', 'MPOS',
       'POPAF', 'Sample.DP']]
a = {'SNV':0,'substitution':1,'deletion':2,'insertion':3}
x['VARIANT_CLASS'] = x['VARIANT_CLASS'].map(a)
b = {'deleterious':0, 'tolerated':1, 'deleterious_low_confidence':2,
       'tolerated_low_confidence':3}
x['SIFT'] = x['SIFT'].map(b)

x['cancer'] = data[['cancer']]
x.to_csv('ROC.csv',index = False)

## correlation heatmap
plt.figure(figsize=(12,10))
cor = x.corr()
sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
plt.show()

# sns.pairplot(x)

fig = sns.pairplot(x)
fig.savefig('pair plot.svg')

#save image
fig.savefig('pair plot.svg',dip = 600)

# train_test and split
y = x[['cancer']] ## target
x = x.drop(['cancer'],axis = 1)
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3)
x_train.shape,y_train.shape

y_train.value_counts().plot.pie(autopct='%.2f')

"""#### graph shows the our class of target is imbalnce and it is balanced using oversampling"""

## OVERSAMPLING
from imblearn.over_sampling import RandomOverSampler

#ros = RandomOverSampler(sampling_strategy=1) # Float
ros = RandomOverSampler(sampling_strategy="not majority") # String
X_train_ros, y_train_ros = ros.fit_resample(x_train, y_train)
y_train_ros = pd.DataFrame(y_train_ros)
ax = y_train_ros.value_counts().plot.pie(autopct='%.2f')
_ = ax.set_title("Over-sampling")

# datasets after balanceing class
X_train_ros.shape, y_train_ros.shape

"""### Decision tree model for imbalance data

"""

classifier= RandomForestClassifier(n_estimators= 10, criterion="entropy")  
classifier.fit(x_train, y_train)
y_pred1 = classifier.predict(x_test)
print(classification_report(y_test, y_pred1))

"""## Decision tree for imbalanced data"""

dtc = DecisionTreeClassifier()
dtc.fit(x_train,y_train)
y_pred = dtc.predict(x_test)
print(classification_report(y_test, y_pred))

"""## Decision tree balanced data"""

dtc = DecisionTreeClassifier()
dtc.fit(X_train_ros,y_train_ros)
y_pred = dtc.predict(x_test)
print(classification_report(y_test, y_pred))

"""### Ramdom forest for balanced data"""

classifier1= RandomForestClassifier(n_estimators= 10, criterion="entropy")  
classifier1.fit(X_train_ros, y_train_ros)
y_pred1 = classifier1.predict(x_test)
print(classification_report(y_test, y_pred1))

"""### model cross validtion for imbalance data"""

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(random_state=42)
model.fit(x_train,y_train)

# Training Cross-validation Models
from sklearn.metrics import make_scorer, recall_score, matthews_corrcoef
from sklearn.model_selection import cross_validate

model_cv = RandomForestClassifier(random_state=42)
cv_scoring = {'MCC': make_scorer(matthews_corrcoef)}
cv = cross_validate(model_cv, x_train, y_train, cv=5, scoring=cv_scoring)

# Apply model to make prediction
from sklearn.metrics import matthews_corrcoef

y_train_pred = model.predict(x_train)
y_test_pred = model.predict(x_test)
y_test_pred
mcc_test = matthews_corrcoef(y_test, y_test_pred)
mcc_cv = cv['test_MCC'].mean()

# Display model performance results
df_labels = pd.Series([ 'MCC_CV', 'MCC_test'], name = 'Performance_metric_names')
df_values = pd.Series([mcc_cv, mcc_test], name = 'Performance_metric_values')
df3 = pd.concat([df_labels, df_values], axis=1)
df3

"""### model cross validataion and test score for balanced data

"""

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(random_state=42)
model.fit(X_train_ros, y_train_ros)

# Training Cross-validation Models
from sklearn.metrics import make_scorer, recall_score, matthews_corrcoef
from sklearn.model_selection import cross_validate

model_cv = RandomForestClassifier(random_state=42)
cv_scoring = {'MCC': make_scorer(matthews_corrcoef)}
cv = cross_validate(model_cv, X_train_ros, y_train_ros, cv=5, scoring=cv_scoring)

# Apply model to make prediction
from sklearn.metrics import matthews_corrcoef

y_train_pred = model.predict(X_train_ros)
y_test_pred = model.predict(x_test)
y_test_pred
#mcc_train = matthews_corrcoef(X_train_ros, y_train_pred)
mcc_test = matthews_corrcoef(y_test, y_test_pred)
mcc_cv = cv['test_MCC'].mean()

# Display model performance results
df_labels = pd.Series([ 'MCC_CV', 'MCC_test'], name = 'Performance_metric_names')
df_values = pd.Series([mcc_cv, mcc_test], name = 'Performance_metric_values')
df3 = pd.concat([df_labels, df_values], axis=1)
df3

"""## testing"""

# def testing(a):
#   o = [a]
#   x1 = data.loc[data['SampleID'].isin(o)] 
#   test = x1[['VARIANT_CLASS','TLOD','shiftscore', 'Sample.AF', 'SIFT','MBQ', 'MFRL', 'MMQ','Sample.AD', 'Sample.F1R2', 'Sample.F2R1', 'DP', 'GERMQ', 'MPOS',
#             'POPAF', 'Sample.DP']]
#   a1 = {'SNV':0,'substitution':1,'deletion':2,'insertion':3}
#   test['VARIANT_CLASS'] = test['VARIANT_CLASS'].map(a1)
#   b1 = {'deleterious':0, 'tolerated':1, 'deleterious_low_confidence':2,
#             'tolerated_low_confidence':3}
#   test['SIFT'].fillna(value = 'tolerated',inplace =True)
#   test['SIFT'] = test['SIFT'].map(b1)
#   y_pp = model.predict(test)
#   y_pp = pd.DataFrame(y_pp)
#   y_pp.value_counts().plot.pie(autopct='%.2f')

# a1 = 'SRR941054'
# testing(a1) ## predicted cancer type

# o = ['SRR941054']
# X = data.loc[data['SampleID'].isin(o)]
# X['cancer'].head(2) ### actual cancer type

# a2 = 'SRR900123'
# testing(a2)

# o = ['SRR900123']
# X = data.loc[data['SampleID'].isin(o)]
# X['cancer'].head(2) ### actual cancer type

y_test

y_test_pred



