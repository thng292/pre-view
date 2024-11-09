import random
import google.generativeai as genai
import json
import pandas as pd

class leetcode_problem:
    def __init__(self):
        generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
        }
        
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction="I have a set of tags for interview question: {'Array',\n 'Backtracking',\n 'Biconnected Component',\n 'Binary Search',\n 'Bit Manipulation',\n 'Bitmask',\n 'Brainteaser',\n 'Breadth-First Search',\n 'Combinatorics',\n 'Concurrency',\n 'Counting',\n 'Data Stream',\n 'Database',\n 'Depth-First Search',\n 'Design',\n 'Divide and Conquer',\n 'Dynamic Programming',\n 'Enumeration',\n 'Eulerian Circuit',\n 'Game Theory',\n 'Geometry',\n 'Graph',\n 'Greedy',\n 'Hash Function',\n 'Hash Table',\n 'Heap',\n 'Interactive',\n 'Iterator',\n 'Line Sweep',\n 'Linked List',\n 'Math',\n 'Matrix',\n 'Memoization',\n 'Minimum Spanning Tree',\n 'Monotonic Queue',\n 'Monotonic Stack',\n 'Number Theory',\n 'Ordered Set',\n 'Prefix Sum',\n 'Probability and Statistics',\n 'Queue',\n 'Quickselect',\n 'Randomized',\n 'Recursion',\n 'Rejection Sampling',\n 'Reservoir Sampling',\n 'Rolling Hash',\n 'Segment Tree',\n 'Shell',\n 'Shortest Path',\n 'Simulation',\n 'Sliding Window',\n 'Sorting',\n 'Stack',\n 'String',\n 'Strongly Connected Component',\n 'Suffix Array',\n 'Tree',\n 'Trie',\n 'Two Pointers',\n 'Union Find'}, and job description, give me tags of question suitable for this job (base on jobTitle, programmingLanguages, jobLevel and skills; these tags must in set of tags i given) output tags only; do not use markdown in your output;output tags separate by ,",
            )
        
        self.data = pd.read_parquet('data\\leetcode_problems_fix.parquet').to_dict(orient='records')

    def getQuesion(self, jobDescription):
        jsonStr = json.dumps(jobDescription, ensure_ascii=False)
        chat_session = self.model.start_chat()
        tags = [s.strip() for s in chat_session.send_message(jsonStr).text.split(',')]
        # print(tags)
        res = []
        weight = []
        if jobDescription['jobLevel'] == 'senior':
            hard = 2
            easy = 0
            med = 1
        elif jobDescription['jobLevel'] == 'junior':
            hard = 1
            easy = 2
            med = 3
        elif jobDescription['jobLevel'] == 'intern':
            hard = 0
            easy = 2
            med = 1
        else:
            hard = 1
            easy = 2
            med = 2

        for d in self.data:
            w = 0
            for tag in tags:
                if tag != '' and d['tags'].find(tag) != -1: 
                    w += 1
            if w > 0:
                res.append(d)
                weight.append(w * w)

        res = random.choices(res, weights=weight, k=10)
        weight = [0] * len(res)
        for i,d in enumerate(res):
            weight[i] = (med if d['difficulty'] == 'Medium' else (hard if d['difficulty'] == 'Hard' else easy))
        return random.choices(res, weights=weight, k=1)[0]
    
'''
genai.configure(api_key='')
lc = leetcode_problem()

jobData = {
    "companyName": "SAVIS DIGITAL",
    "jobTitle": "Software Developer (Backend)",
    "jobLevel": "senior",
    "yoe": 3,
    "programmingLanguages": ["Java"],
    "frameworks": [],
    "skills": [
        "Backend development",
        "API ecosystem development",
        "WSO2 API Manager",
        "OpenAPI",
        "OpenShift",
        "Kubernetes (K8s)",
        "Algorithms and protocols (RSA, AES, SHA, TLS/SSL, Mutual SSL)",
        "Digital signature and encryption for data protection",
        "Troubleshooting",
        "Problem-solving"
    ],
    "responsibilities": [
        "Develop software products and build API ecosystems for banking",
        "Contribute to API ecosystem development following OpenAPI standards",
        "Research and apply new technologies",
        "Program complex modules and integrate with other modules",
        "Interact with solution architects for project requirements and design",
        "Build and package products for different versions",
        "Document design specifications and functionalities",
        "Deliver software products on time and with quality"
    ]
}
print(lc.getQuesion(jobData))
'''