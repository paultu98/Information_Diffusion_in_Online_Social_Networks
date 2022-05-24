# coding = utf-8
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import decomposition
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
import random
from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import BorderlineSMOTE
from collections import Counter

# Resampling and model construction (SMOTE, MLP) (level 2 - Step 7)
# combine 3 tables
data1 = pd.read_table("C:/Users/admin/Desktop/new_data_final/data1130677950_24-10new.txt")
print(data1.shape)
data2 = pd.read_table("C:/Users/admin/Desktop/new_data_final/data1850988623_33-10new.txt")
print(data2.shape)
data3 = pd.read_table("C:/Users/admin/Desktop/new_data_final/data2482557597_33-10new.txt")
print(data3.shape)
final = data1.append(data2).append(data3)
print(final.shape)
# frequency of 0 and 1
print(sum(final['repost']), final.shape[0] - sum(final['repost']),
      sum(final['repost']) / (final.shape[0] - sum(final['repost'])))

# divide into 0 and 1
data_0 = final[final['repost'] == 0]
print(data_0.shape)
data_1 = final[final['repost'] == 1]
print(data_1.shape)

# simple random sample 0
data_0 = data_0.sample(n=20000, replace=False, random_state=3, axis=0) # random sample
print(data_0.shape)

# combine
final = data_1.append(data_0)
print(final.shape)
# split into x and y
y = final["repost"]
n = len(y)
print(n)
y = np.reshape(y, [n, ])
x = final.drop(columns=["repost"])
x = x.values  # get the x(np.array)
print(x.shape)

# SMOTE
x_smo, y_smo = SMOTE(random_state=3).fit_sample(x, y)
print(Counter(y_smo))

# standardization
scaler = preprocessing.StandardScaler()
scaler.fit(x_smo)
x_smo = scaler.transform(x_smo)
x_smo = pd.DataFrame(x_smo)

print('x: ', x_smo.shape)  # print the size of x
print('y: ', y_smo.shape)  # print the size of y

xtrain, xtest, ytrain, ytest = train_test_split(x_smo, y_smo)  # split the data
clf = MLPClassifier(hidden_layer_sizes=(20, 15, 10), activation='tanh', solver='adam',
                    alpha=0.0001, batch_size='auto', learning_rate='constant',
                    learning_rate_init=0.001, power_t=0.5, max_iter=10000, shuffle=True,
                    random_state=5, tol=0.0000001, verbose=True, warm_start=True,
                    momentum=0.8, nesterovs_momentum=True, early_stopping=False,
                    validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-06,n_iter_no_change=10000)

clf.fit(xtrain, ytrain)  # train the classifier
resulr = clf.predict(xtrain)
result = clf.predict(xtest)

print('train confusion_matrix\n', confusion_matrix(ytrain, resulr))
print(classification_report(ytrain, resulr))
print('test confusion_matrix\n', confusion_matrix(ytest, result))
print(classification_report(ytest, result))
