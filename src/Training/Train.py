# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:56:20 2019

@author: Daniel Jimenez
"""
import os
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as dates

from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report
from sklearn.neural_network import MLPClassifier
import numpy as np
import pickle

main_path = os.path.abspath(__file__+"/../../..")+"/"

# Se carga el archivo.csv de la base de datos
file = main_path+'Data/'+ 'Ciclo_3.csv'
data2 = pd.read_csv(file, usecols=['field1','field2','field5','field3'])
target=data2.field5
x1 = data2.field1
x2 = data2.field2
x3 = data2.field3

# Se estandariza los datos para SGDClassifier y MLPClassifier
x1_mean = np.mean(x1)
x1_std = np.std(x1)
x1_est = (x1 - x1_mean)/x1_std
x2_mean = np.mean(x2)
x2_std = np.std(x2)
x2_est = (x2 - x2_mean)/x2_std
x3_mean = np.mean(x3)
x3_std = np.std(x3)
x3_est = (x3 - x3_mean)/x3_std


N=len(x1)


X=np.zeros([N,3])
Y=np.zeros([N,1])

X_EST=np.zeros([N,3])
Y_EST=np.zeros([N,1])


Y[:,0]=target
X[:,0]=x1
X[:,1]=x2
X[:,2]=x3

Y_EST[:,0]=target
X_EST[:,0]=x1_est
X_EST[:,1]=x2_est
X_EST[:,2]=x3_est


# TRainning

# Ababoost

clf_ada = AdaBoostClassifier(n_estimators=1500,learning_rate=0.01,random_state=10)

# Ciclo 1 GradientBoostingClassifier

#clf_GDB = GradientBoostingClassifier(learning_rate=1, n_estimators=1500,max_depth=4, min_samples_split=40, min_samples_leaf=7, subsample=1, max_features='sqrt', random_state=10)

# Ciclo 2 y 3 GradientBoostingClassifier
clf_GDB = GradientBoostingClassifier(learning_rate=0.01, n_estimators=1500,max_depth=4, min_samples_split=40, min_samples_leaf=7, subsample=1, max_features='sqrt', random_state=10)

#SGDClassifier

clf_SGD = SGDClassifier(alpha=0.0001, average=False, class_weight=None, epsilon=0.1,
       eta0=0.0, fit_intercept=True, l1_ratio=0.15,
       learning_rate='optimal', loss='hinge', n_iter=5,n_jobs=1,
       penalty='l2', power_t=0.5, random_state=0, shuffle=True,
       verbose=10, warm_start=False)

# CICLO 1 y 3 MLPClassifier
clf_NN = MLPClassifier(hidden_layer_sizes=(150,150,150), max_iter=500, alpha=0.0001,solver='adam', verbose=10,  random_state=21,tol=0.0000001)


# CICLO 2 MLPClassifier
#clf_NN = MLPClassifier(hidden_layer_sizes=(100,100,100), max_iter=1000, alpha=0.0001, solver='adam', verbose=10,  random_state=21,tol=0.00000001)



# 70% de los datos para entrenamiento
train=int(N*0.70)
X_train = X[0:train]
Y_train = Y[0:train]
X_val = X[train:N]
Y_val = Y[train:N]
Nval=len(X_val)
Nval2=len(X_train)

X_train_Est = X_EST[0:train]
Y_train_Est = Y_EST[0:train]
X_val_Est = X_EST[train:N]
Y_val_Est = Y_EST[train:N]

clf_ada.fit(X_train,Y_train) # Ababoost
clf_GDB.fit(X_train,Y_train) # GradientBoosting
clf_SGD.fit(X_train_Est,Y_train_Est) #	SGDClassifier
clf_NN.fit(X_train_Est,Y_train_Est) # 	MLPClassifier




#Archivo DATA
path2 = main_path+"Data\\"+"Learning_models\\"+'finalized_model1.sav'
filename = open(path2,'wb')
pickle.dump(clf_ada, filename) # Guarda el entrenamiento de Adaboost
filename.close()
#

# Prediccion de Adaboost
pred0_ada=np.zeros([Nval,1])
pred0_ada[:,0]=clf_ada.predict(X_val)
# Prediccion de GradientBoosting
pred0_GDB=np.zeros([Nval,1])
pred0_GDB[:,0]=clf_GDB.predict(X_val)
# Prediccion de SGDClassifier
pred0_SDG=np.zeros([Nval,1])
pred0_SDG[:,0]=clf_SGD.predict(X_val_Est)
# Prediccion de MLPClassifier
pred0_NN=np.zeros([Nval,1])
pred0_NN[:,0]=clf_NN.predict(X_val_Est)

# F1-score de los clasificadores
f1_ada=f1_score(Y_val,pred0_ada, average =None)
f1_GDB=f1_score(Y_val,pred0_GDB, average =None)
f1_SDG=f1_score(Y_val,pred0_SDG, average =None)
f1_NN=f1_score(Y_val,pred0_NN, average =None)
