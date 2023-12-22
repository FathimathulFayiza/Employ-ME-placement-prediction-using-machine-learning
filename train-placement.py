import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,confusion_matrix

dataset=pd.read_csv('project_data_EC.csv')

X=np.array(dataset.iloc[:,:-1])
X=X.astype(dtype='int')
Y=np.array(dataset.iloc[:,-1])
# Y=Y.astype(dtype='str')
Y=Y.reshape(-1,)
print(X)
print(Y)
print(Y.shape)
X_train, X_test, y_train, y_test =train_test_split(X,Y,test_size=0.25,random_state=42)

print(X_train.shape)
model_RR=RandomForestClassifier(n_estimators=100,criterion='entropy',)
model_RR.fit(X_train,y_train)
y_predicted_RR=model_RR.predict(X_test)
confusion=confusion_matrix(y_test,y_predicted_RR)
print('Accuracy :')
print(accuracy_score(y_test,y_predicted_RR))