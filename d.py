from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import joblib

df_nptel = pd.read_csv('data/nptel.csv')
df_mit = pd.read_csv('data/mit.csv')
df_udemy = pd.read_csv('data/udemyN.csv')
df_coursera = pd.read_csv('data/coursera.csv')

# Define functions
def get_relevant_courses_from_cluster_nptel(query, dataframe=df_nptel, top_n=5):
    vectorizer_nptel = joblib.load('model/vectorizer_nptel.pkl')
    km_nptel = joblib.load('model/km_nptel.pkl')
    query_vec = vectorizer_nptel.transform([query])
    cluster_label = km_nptel.predict(query_vec)[0]
    cluster_courses = dataframe[dataframe['cluster'] == cluster_label]
    course_vecs = vectorizer_nptel.transform(cluster_courses['TRAIN'])
    similarity_scores = cosine_similarity(query_vec, course_vecs).flatten()
    cluster_courses['similarity'] = similarity_scores
    cluster_courses = cluster_courses.sort_values(by='similarity', ascending=False)
    return cluster_courses[['Course Name', 'NPTEL URL']].head(top_n)

def get_relevant_courses_from_cluster_mit(query, dataframe=df_mit, top_n=5):
    vectorizer_mit = joblib.load('model/vectorizer_mit.pkl')
    km_mit = joblib.load('model/km_mit.pkl')
    query_vec = vectorizer_mit.transform([query])
    cluster_label = km_mit.predict(query_vec)[0]
    cluster_courses = dataframe[dataframe['cluster'] == cluster_label]
    course_vecs = vectorizer_mit.transform(cluster_courses['TRAIN'])
    similarity_scores = cosine_similarity(query_vec, course_vecs).flatten()
    cluster_courses['similarity'] = similarity_scores
    cluster_courses = cluster_courses.sort_values(by='similarity', ascending=False)
    return cluster_courses[['Course Title', 'URL']].head(top_n)

def get_relevant_courses_from_cluster_udemy(query, dataframe=df_udemy, top_n=5):
    vectorizer_udemy = joblib.load('model/vectorizer_udemy.pkl')
    km_udemy = joblib.load('model/km_udemy.pkl')
    query_vec = vectorizer_udemy.transform([query])
    cluster_label = km_udemy.predict(query_vec)[0]
    cluster_courses = dataframe[dataframe['cluster'] == cluster_label]
    course_vecs = vectorizer_udemy.transform(cluster_courses['title'])
    similarity_scores = cosine_similarity(query_vec, course_vecs).flatten()
    cluster_courses['similarity'] = similarity_scores
    cluster_courses = cluster_courses.sort_values(by='similarity', ascending=False)
    return cluster_courses[['title', 'course_url']].head(top_n)

def get_relevant_courses_from_cluster_coursera(query, dataframe=df_coursera, top_n=5):
    vectorizer_coursera = joblib.load('model/vectorizer_coursera.pkl')
    km_coursera = joblib.load('model/km_coursera.pkl')
    query_vec = vectorizer_coursera.transform([query])
    cluster_label = km_coursera.predict(query_vec)[0]
    cluster_courses = dataframe[dataframe['cluster'] == cluster_label]
    course_vecs = vectorizer_coursera.transform(cluster_courses['TRAIN'])
    similarity_scores = cosine_similarity(query_vec, course_vecs).flatten()
    cluster_courses['similarity'] = similarity_scores
    cluster_courses = cluster_courses.sort_values(by='similarity', ascending=False)
    return cluster_courses[['Course Title', 'Course Url']].head(top_n)
# Ensure that the data loading and model training are only executed when the script is run directly
if __name__ == "__main__":
    user_query = "Robotics"
    relevant_courses_nptel = get_relevant_courses_from_cluster_nptel(user_query)
    print(f"Top {len(relevant_courses_nptel)} courses related to '{user_query}' from NPTEL:")
    print(relevant_courses_nptel)

    relevant_courses_mit = get_relevant_courses_from_cluster_mit(user_query)
    print(f"Top {len(relevant_courses_mit)} courses related to '{user_query}' from MIT:")
    print(relevant_courses_mit[['Course Title', 'URL']])

    relevant_courses_udemy = get_relevant_courses_from_cluster_udemy(user_query)
    print(f"Top {len(relevant_courses_udemy)} courses related to '{user_query}' from Udemy:")
    print(relevant_courses_udemy)

    relevant_courses_coursera = get_relevant_courses_from_cluster_coursera(user_query)
    print(f"Top {len(relevant_courses_coursera)} courses related to '{user_query}' from Coursera:")
    print(relevant_courses_coursera[['Course Title', 'Course Url']])