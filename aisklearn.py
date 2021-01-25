import pandas as pd
from pandas import ExcelWriter
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt

import numpy as np
import datetime

import sklearn
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.datasets import load_iris
import joblib


kn = 3

def sk_learn(ti_df, sheet):
    #for sklearn analysis
    
    target= ti_df['Bid']
    ti_df = ti_df.drop(['Bid','Date','Price', 'Bid1'],axis=1)
    data = ti_df
##    dataset = sklearn.datasets.base.Bunch(data=data, target=target)
    X = data
    y = target
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.3)
    model = KNeighborsClassifier(n_neighbors = kn)
    model.fit(X_train, y_train)
    joblib.dump(model, "models/"+sheet+"_knn_model")
    y_pred = model.predict(X_test)
    m = metrics.accuracy_score(y_test, y_pred)
    print('Probability of', sheet, 'is', m)
    prediction = model.predict(ti_df)
    
    #print(main_copy['Predictions'])

##    print(sheet, main_copy['AI Predictions'][0])

    return prediction
