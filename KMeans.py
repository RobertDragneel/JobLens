import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

dataset = pd.read_csv('jobs.csv')

#remove all listed with no listed skills
dataset['skills'] = dataset['skills'].fillna('')
dataset = dataset[dataset['skills'] != '']

#convert skills string to list object
dataset['skills_list'] = dataset['skills'].apply(lambda x: [skill.strip() for skill in x.split(',') if skill.strip()])

#convert skill list into numeric
mlb = MultiLabelBinarizer()
X = mlb.fit_transform(dataset['skills_list'])

#find number of clusters with silhouette score
sil_scores = []
k_range = range(2, 10)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X)
    score = silhouette_score(X, labels)
    sil_scores.append(score)

#sil score plot
plt.figure(figsize=(6,4))
plt.plot(k_range, sil_scores, marker='o')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score vs Number of Clusters')
plt.show()

#find best k with highest sil score
best_k = k_range[np.argmax(sil_scores)]

#run kmeans
kmeans = KMeans(n_clusters=best_k, random_state=42)
dataset['cluster'] = kmeans.fit_predict(X)

#create cluster labels based on top skills
cluster_labels = {}

for cluster_num in range(best_k):
    cluster_skills = X[dataset['cluster']==cluster_num].sum(axis=0)
    top_skills_idx = np.argsort(cluster_skills)[::-1][:5]
    top_skills = [mlb.classes_[i] for i in top_skills_idx]

    #creates labels
    if any(skill.lower() in ['python', 'tensorflow', 'pytorch', 'ml', 'ai'] for skill in top_skills):
        label = "ML/AI"
    elif any(skill.lower() in ['aws', 'gcp', 'azure', 'docker', 'kubernetes', 'ci/cd', 'terraform'] for skill in top_skills):
        label = "Cloud/DevOps"
    elif any(skill.lower() in ['go', 'typescript', 'grpc', 'rest'] for skill in top_skills):
        label = "Backend/Software Engineering"
    else:
        label = "Other"
    cluster_labels[cluster_num] = label

dataset['cluster_label'] = dataset['cluster'].map(cluster_labels)

#assign jobs to clusters
for cluster_num in range(best_k):
    cluster_skills = X[dataset['cluster']==cluster_num].sum(axis=0)
    top_skills_idx = np.argsort(cluster_skills)[::-1][:10]  
    top_skills = [mlb.classes_[i] for i in top_skills_idx]