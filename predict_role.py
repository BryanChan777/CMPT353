import sys
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.preprocessing import LabelEncoder

OUTPUT_TEMPLATE = (
    'Model score: {score:.3g}\n'
)

def main():
    data = pd.read_csv('owl_playerstats.csv').drop(columns=['name', 'team', 'teamId'])
    
    X_1 = data.drop(columns=['role']).loc[:,'playerId':'time_played_total'].values
    y_1 = data.role.values

    X1_train, X1_test, y1_train, y1_test = train_test_split(X_1, y_1)

    model = make_pipeline(
    	StandardScaler(),
    	VotingClassifier([
            ('nb', GaussianNB()),
            ('knn', KNeighborsClassifier(9)),
            ('svc', SVC(kernel='linear', C=0.1)),
            ('rand_forest', RandomForestClassifier(
                    n_estimators=175, 
                    criterion="gini", 
                    max_depth=25, 
                    min_samples_split=2, 
                    min_samples_leaf=25, 
                    min_weight_fraction_leaf=0.0, 
                    max_features="auto", 
                    max_leaf_nodes=None, 
                    min_impurity_decrease=0.0, 
                    min_impurity_split=None, 
                    bootstrap=True, 
                    oob_score=False, 
                    n_jobs=None, 
                    random_state=None, 
                    verbose=0, 
                    warm_start=False, 
                    class_weight=None
                )
            )
        ], voting = 'hard')
    )

    model.fit(X1_train, y1_train)

    # monthly_unlabelled = pd.read_csv(sys.argv[2])

    X_2 = data.drop(columns=['role']).loc[:,'playerId':'time_played_total'].values
    # pd.Series(model.predict(X_2)).to_csv(sys.argv[3], index=False)
    print(model.predict(X_2))

    print(OUTPUT_TEMPLATE.format(
            score = model.score(X1_test, y1_test) 
        )
    )

    # hint for question 2 of answers.txt
    # df = pd.DataFrame({
    #     'truth': y1_train, 
    #     'prediction': model.predict(X1_train)
    # })
    # print(df[df['truth'] != df['prediction']])

if __name__ == '__main__':
    main()