import csv
import pandas as pd
import numpy as np
import json

dataset = pd.read_csv('jobs_with_skills.csv')

#remove all listed with zero skills
dataset['skills'] = dataset['skills'].where(pd.notnull(dataset['skills']), None)
dataset = dataset[dataset['skill_count'] != 0]

#print((dataset['skill_count'] == 0).sum()) #testing

#convert json object of skills to list
dataset['data_dict'] = dataset['skill_counts_json'].apply(json.loads)
dataset['skill_list'] = dataset['data_dict'].apply(lambda x: [k.lower() for k in x.keys()])

#user input for skill search
skills_input = input("Enter skills to search for (comma-separated): ")
skills_search = [skill.strip().lower for skill in skills_input.split(',')]

#query list in row for input skills
def has_match(data_values, search_values_set):
    return any(val in search_values_set for val in data_values)

search_values_set = set(skills_search)
#filters dataset to search values
matching_rows = dataset[dataset['skill_list'].apply(lambda x: has_match(x, search_values_set))]

print(matching_rows) #temp output
