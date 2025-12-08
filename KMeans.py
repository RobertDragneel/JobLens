import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

dataset = pd.read_csv('jobs_with_skills.csv')

#remove all listed with zero skills
dataset['skills'] = dataset['skills'].where(pd.notnull(dataset['skills']), None)
dataset = dataset[dataset['skill_count'] != 0]

