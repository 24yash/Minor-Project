# app.py
from flask import Flask, render_template, request
from fns import (get_relevant_courses_from_cluster_nptel, 
                get_relevant_courses_from_cluster_mit,
                get_relevant_courses_from_cluster_udemy, 
                get_relevant_courses_from_cluster_coursera)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        nptel_results = get_relevant_courses_from_cluster_nptel(query)
        mit_results = get_relevant_courses_from_cluster_mit(query)
        udemy_results = get_relevant_courses_from_cluster_udemy(query)
        coursera_results = get_relevant_courses_from_cluster_coursera(query)
        
        return render_template('results.html', 
                             query=query,
                             nptel_results=nptel_results,
                             mit_results=mit_results, 
                             udemy_results=udemy_results,
                             coursera_results=coursera_results)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)