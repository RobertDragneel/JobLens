import csv
import pandas as pd
import numpy as np

dataset = pd.read_csv('jobs_with_skills.csv')

#remove all listed with zero skills
dataset['skills'] = dataset['skills'].where(pd.notnull(dataset['skills']), None)
dataset = dataset[dataset['skill_count'] != 0]

print((dataset['skill_count'] == 0).sum()) #testing
