import sys
import random
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
'''
1) get unlabelled validation players with correct roles
2) get unlabelled validation players with correct team

3) get unlabelled validation players with predicted roles
4) get unlabelled validaiton players with predicted team
# use parameter c=role/team in plt.scatter(y,x,c)
5) plt.scatter unlabelled validation with correct roles/team
6) plt.scatter unlabelled validation with predicted roles/teaam

'''
def role_color(role):
    if(role == 'offense'):
        return (0.3,0.3,0.3)
    if(role == 'tank'):
        return (0.3,0.3,0.3)
    if(role == 'support'):
        return (0.3,0.3,0.3)
    
def team_color(team):
    return

def main():
    roles = pd.read_csv('roles_predicted.csv')
    teams = pd.read_csv('team_predicted.csv')
    
    
    roles = 
    #visualization of predict.py files
    plt.scatter(roles['hero_damage_avg_per_10m'].values, roles['healing_avg_per_10m'].values, c=roles['role'])
    plt.show()
    
    plt.scatter(roles['hero_damage_avg_per_10m'].values, roles['healing_avg_per_10m'].values, c=roles['prediction'])
    plt.show()
    #prediction from

if __name__ == '__main__':
    main()
