import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB

def main():
    data_labelled = pd.read_csv('owl_playerstats.csv')
    print(data_labelled)

    cleaned_data = data_labelled.drop(columns=['role','team', 'teamId', 'playerId', 'name'])
    data_unlabelled = cleaned_data

    print(data_unlabelled)
    X = cleaned_data.values
    y= data_labelled['name'].values
    
    X_train, X_valid, y_train, y_valid = train_test_split(X, y)
    
    #testing different diff ml models for the highest score
    knn_model = make_pipeline(
        StandardScaler(),
        KNeighborsClassifier(n_neighbors=9)
    )
    knn_model.fit(X_train, y_train)
    
    svc_model = make_pipeline(
        	StandardScaler(),
        	SVC(kernel='linear', C=0.1)
        )
    svc_model.fit(X_train, y_train)
    
    rf_model = make_pipeline(
        	StandardScaler(),
            RandomForestClassifier(n_estimators=300,
            max_depth=7, min_samples_leaf=7)
            )
    rf_model.fit(X_train, y_train)
    
    gb_model = make_pipeline(
        	StandardScaler(),
        GaussianNB()
            )
    gb_model.fit(X_train, y_train)
    
    X_unlabelled = data_unlabelled.values
    predictions = svc_model.predict(X_unlabelled)  
    predictions2 = knn_model.predict(X_unlabelled) 
    predictions3 = rf_model.predict(X_unlabelled)  
    predictions4 = gb_model.predict(X_unlabelled)
    print(svc_model.score(X_valid, y_valid))
    print(knn_model.score(X_valid, y_valid))
    print(rf_model.score(X_valid, y_valid))
    print(gb_model.score(X_valid, y_valid))

    #pd.Series(predictions).to_csv(sys.argv[3], index=False, header=False)
    print(predictions)


if __name__ == '__main__':
    main()