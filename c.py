import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to extract the description from the URL
def get_description(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the div with class 'content-inner'
        content_inner = soup.find('div', class_='content-inner')

        # If content_inner is not found, it indicates the link is broken or course is expired
        if content_inner is None:
            return None

        # Initialize an empty list to store the text of <p> tags
        paragraphs = []

        # Find all <p> tags within the 'content-inner' div
        p_tags = content_inner.find_all('p')

        # Extract and append the text from each <p> tag
        for p in p_tags:
            paragraphs.append(p.get_text(strip=True))

        # Join all paragraph texts into a single string separated by spaces
        description = ' '.join(paragraphs)

        return description

    except Exception as e:
        # If there's an issue with the request, return None to indicate failure
        return None

# Function to update descriptions in the DataFrame
def update_descriptions(df):
    # Create a list to store the indices of rows with broken links
    indices_to_delete = []
    i = 0

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        if i%50==0:
          print(i)
        i+=1
        # Get the URL from the 'Course Url' column
        url = row['Course Url']

        # Get the description from the URL
        description = get_description(url)

        # If the description is None, mark the index for deletion (broken link)
        if description is None:
            indices_to_delete.append(index)
        else:
            # Update the DataFrame with the description
            df.at[index, 'Description'] = description

        # Add a short delay of 0.005 seconds between each request
        time.sleep(0.005)
        
    print('done')

    # Drop rows with broken links (those marked for deletion)
    df.drop(indices_to_delete, inplace=True)

# Example usage:
if __name__ == "__main__":
    # Load the dataset from a CSV file
    df = pd.read_csv('CourseraDataset.csv')
    # data = {'Course Url': ['https://www.coursera.org/learn/fashion-design', 'https://www.coursera.org/learn/modern-american-poetry']}
    # df = pd.DataFrame(data)

    # Update the DataFrame with descriptions
    update_descriptions(df)

    # Save the updated DataFrame to a new CSV file (optional)
    df.to_csv('Updated_CourseraDataset.csv', index=False)

    # Display the updated DataFrame
    print(df.head())
