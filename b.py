from d import get_relevant_courses_from_cluster_nptel, get_relevant_courses_from_cluster_mit, get_relevant_courses_from_cluster_udemy

user_query = "Machine Learning"

# relevant_courses_nptel = get_relevant_courses_from_cluster_nptel(user_query)
# print(f"Top {len(relevant_courses_nptel)} courses related to '{user_query}' from NPTEL:")
# print(relevant_courses_nptel[['Course Name', 'NPTEL URL', 'similarity']])

relevant_courses_mit = get_relevant_courses_from_cluster_mit(user_query)
print(f"Top {len(relevant_courses_mit)} courses related to '{user_query}' from MIT:")
print(relevant_courses_mit[['Course Title', 'URL', 'similarity']])

# relevant_courses_udemy = get_relevant_courses_from_cluster_udemy(user_query)
# print(f"Top {len(relevant_courses_udemy)} courses related to '{user_query}' from Udemy:")
# print(relevant_courses_udemy[['course_title', 'url', 'similarity']])