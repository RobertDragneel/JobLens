import csv
import pandas as pd
import numpy as np

dataset = pd.read_csv('jobs_with_skills.csv')

#need to either remove all listed with zero skills or just clean 
dataset['skills'] = dataset['skills'].where(pd.notnull(dataset['skills']), None)

print(dataset.loc[1,'skills'])
