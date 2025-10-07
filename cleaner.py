import csv
import pandas as pd
import numpy as np
import json

dataset = pd.read_csv('jobs_with_skills.csv')

#remove all listed with zero skills
dataset['skills'] = dataset['skills'].where(pd.notnull(dataset['skills']), None)
dataset = dataset[dataset['skill_count'] != 0]

#print((dataset['skill_count'] == 0).sum()) #testing

skills_search = ['Java', 'CSS'] #temp

dataset['data_dict'] = dataset['skill_counts_json'].apply(json.loads)
dataset['skill_list'] = dataset['data_dict'].apply(lambda x: list(x.keys()))

def has_match(data_values, search_values_set):
    return any(val in search_values_set for val in data_values)

search_values_set = set(skills_search)
matching_rows = dataset[dataset['skill_list'].apply(lambda x: has_match(x, search_values_set))]

print(matching_rows)