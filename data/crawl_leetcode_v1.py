import requests
from bs4 import BeautifulSoup
import json
import time
import csv



def remove_code_tag_html(html_description):
    soup = BeautifulSoup(html_description, 'html.parser')
    for tag in soup.find_all('code'):
        tag.unwrap()
    return soup


# URL for LeetCode's problem list
url = "https://leetcode.com/api/problems/all/"

# Get the JSON data from the API
response = requests.get(url)
data = response.json()

# Parsing problem information
problems = data['stat_status_pairs']

# LeetCode GraphQL endpoint to get problem details
graphql_url = "https://leetcode.com/graphql"

# Collect all problems with their description, difficulty, and tags
problem_list = []

index = 0
for problem in problems:
    title = problem['stat']['question__title']
    difficulty = problem['difficulty']['level']  # 1 - Easy, 2 - Medium, 3 - Hard
    slug = problem['stat']['question__title_slug']
    paid_only = problem['paid_only']  # if the problem is premium (True or False)
    
    # GraphQL query to get the detailed problem info, including description and tags
    query = {
        "query": """
        query getQuestionDetail($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                title
                content
                difficulty
                topicTags {
                    name
                }
            }
        }
        """,
        "variables": {
            "titleSlug": slug
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # Retry logic to handle rate-limiting
    retry_count = 0
    while retry_count < 3:
        detail_response = requests.post(graphql_url, json=query, headers=headers)
        
        if detail_response.status_code == 200:
            break
        else:
            retry_count += 1
            print(f"Rate limited. Retrying in {retry_count * 2} seconds...")
            time.sleep(retry_count * 2)  # Exponential backoff

    if detail_response.status_code == 200:
        detail_data = detail_response.json()
        question_data = detail_data['data']['question']
        description_html = question_data['content']
        # Check if description_html is not None before parsing
        if description_html:
            description = remove_code_tag_html(description_html).get_text()
            
        else:
            description = "No description available."


        tags = [tag['name'] for tag in question_data['topicTags']]
    else:
        description = "Could not fetch description"
        tags = []
    
    # Map difficulty level to text
    difficulty_map = {1: 'Easy', 2: 'Medium', 3: 'Hard'}
    difficulty_text = difficulty_map.get(difficulty, 'Unknown')
    
    # Append the problem details
    problem_list.append({
        'title': title,
        'description': description,
        'difficulty': difficulty_text,
        'tags': tags,
        'paid_only': paid_only
    })

    time.sleep(1)
    print(f"{title} processed.")


# Save into csv file
with open('leetcode_problems.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Description', 'Difficulty', 'Tags', 'Paid Only'])
    for problem in problem_list:
        writer.writerow([problem['title'], problem['description'], problem['difficulty'], ', '.join(problem['tags']), problem['paid_only']])
        print(f"{problem['title']} saved to CSV file.")
    
