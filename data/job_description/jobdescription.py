from dotenv import load_dotenv
import json
import datasets

load_dotenv("../.env")

PROMT_SYSTEM = "You are a senior developer"
PROMT_TEMPLATE = """This is a job description of a job related to IT field:
-----------------------------------
{}
-----------------------------------
Your task is to extract the following information from the above paragraph and export it to valid json:
- Company name
- Job title
- Job level (intern, fresher, junior, senior)
- Year of experiences (yoe)
- Programming languages
- Frameworks
- Skills (technical skill only)
- Responisbilities
- Problem tag
- Problem difficulty
- Interview topics

Problem tag is the kind of problems the interviewer should ask the candidate, based on the job title, job level and experiences. All available task: Hash Table, Math, Two Pointers, Depth-First Search, Stack, Number Theory, Game Theory, Linked List, Tree, Dynamic Programming, Memoization, Reservoir Sampling, Trie, Set, Matrix, Greedy, Recursion, Graph, Bitmask, Union Find, Queue, Breadth-First Search, Divide and Conquer, Sorting, String, Backtracking, Binary Search, Array, Prefix Sum, Geometry, Shortest Path, Priority Queue, Sliding Window

Problem diffifulty is the difficulty of the questions to ask the candidate, this should based on the year of experiences and job level. It must be one of easy, medium, hard

Interview topics is the topic of questions the interviewer can use to ask the candidate

For example, with this job description:
-----------------------------------
Leader in the development and publishing of games, Gameloft® has established itself as a pioneer in the industry, creating innovative gaming experiences for over 20 years. Gameloft creates games for all digital platforms, from mobile to cross-platform titles for PC and consoles. Gameloft operates its own established franchises such as Asphalt®, Dragon Mania Legends, Modern Combat and Dungeon Hunter and also partners with major rights holders including LEGO®, Universal, Illumination Entertainment, Hasbro®, Fox Digital Entertainment, Mattel®, Lamborghini®, and Ferrari®. Gameloft distributes its games in over 100 countries and employs 2,700 people worldwide. Every month, 55 million unique users can be reached by advertisers in Gameloft games with Gameloft for brands, a leading B2B offering dedicated to brands and agencies. Gameloft is a Vivendi company. 

An Intern will learn and be trained
    C++ programming & OPP knowledge.
    Game features in Gameloft games.
    After the initial training period, the intern will join on-the-job training - work directly with the team on practical projects.
    Proposing ideas to contribute to the development of the team, department and studio in general.

Qualifications
    Final year students/fresh graduates from IT major; able to work full-time
    C++ programming & OOP knowledge
    Good logical thinking & willingness to learn
    Have a passion for programming, especially mobile game programming
    English proficiency is an advantage.
-----------------------------------

The output should be:
{{
    "companyName": "Gameloft",
    "jobTitle": "Game developer",
    "jobLevel": "intern",
    "yoe": 0
    "programmingLanguages": ["C++"],
    "frameworks": []
    "skills": [
        "Object Oriented Programming",
        "Logical thinking",
        "Willingness to learn",
        "Mobile game programming"
    ],
    "responsibilities": [
        "Contribute to the development of the team",
    ],
    "problems": ["Stack", "Hash table", "Array"],
    "difficulty": "easy"
    "topics": ["OOP", "C++", "Object lifetime"]
}}
"""

data = datasets.load_dataset("pre-view/JD-IT-linkedin-topcv")
batch = []
for i, jd in enumerate(data['train']['content']):
    batch.append({
        "custom_id": f"jd-{i}",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            # This is what you would have in your Chat Completions API call
            "model": "gpt-4o",
            "response_format": {
                "type": "json_object"
            },
            "messages": [
                {
                    "role": "system",
                    "content": PROMT_SYSTEM
                },
                {
                    "role": "user",
                    "content": PROMT_TEMPLATE.format(jd)
                }
            ]
        }
    })

with open("batch.jsonl", 'w') as f:
    for bb in batch:
        f.write(json.dumps(bb) + '\n')
