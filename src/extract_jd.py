from enum import Enum
from pydantic import BaseModel
from google.generativeai import GenerativeModel, GenerationConfig
import json

SYSTEM_INSTRUCTION = """You are a helpful assistant. You will receive job description related to IT from the user, your job is to extract the information in the given IT job description. Only use the information provided in the job description. Here are some hint for the json fields:
- companyName: the name of the company
- jobTitle: the job title
- jobLevel: the experience level required for the job (intern, junior, ...)
- yoe: year of experiences required for the job
- programmingLanguages: the programming language(s) listed in the job description
- frameworks: the framework(s) listed in the job description
- skills: the skills that the candidate should have
- responsibilities: the job's responsibilities
- problems: what type of problem should the interviewer ask the candidate in coding interview to know if he fit the requirements
- problemDifficulty: what should be the difficulty of the above question
- interviewTopics: what should the interviewer ask the candidate during the interview
"""

model = GenerativeModel("gemini-1.5-flash-002", system_instruction=SYSTEM_INSTRUCTION)


class ProblemTag(str, Enum):
    hashTable = "Hash Table"
    math = "Math"
    twoPointers = "Two Pointers"
    depthFirstSearch = "Depth-First Search"
    stack = "Stack"
    numberTheory = "Number Theory"
    gameTheory = "Game Theory"
    linkedList = "Linked List"
    tree = "Tree"
    dynamicProgramming = "Dynamic Programming"
    memoization = "Memoization"
    reservoirSampling = "Reservoir Sampling"
    trie = "Trie"
    set = "Set"
    matrix = "Matrix"
    greedy = "Greedy"
    recursion = "Recursion"
    graph = "Graph"
    bitmask = "Bitmask"
    unionFind = "Union Find"
    queue = "Queue"
    breadthFirstSearch = "Breadth-First Search"
    divideAndConquer = "Divide and Conquer"
    sorting = "Sorting"
    string = "String"
    backtracking = "Backtracking"
    binarySearch = "Binary Search"
    array = "Array"
    prefixSum = "Prefix Sum"
    geometry = "Geometry"
    shortestPath = "Shortest Path"
    priorityQueue = "Priority Queue"
    slidingWindow = "Sliding Window"


class JobLevel(str, Enum):
    intern = "intern"
    fresher = "fresher"
    junior = "junior"
    mid_level = "mid-level"
    senior = "senior"


class ProblemDifficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class JobExtractedOutput(BaseModel):
    companyName: str | None
    jobTitle: str
    jobLevel: JobLevel
    yoe: int
    programmingLanguages: list[str]
    frameworks: list[str]
    skills: list[str]
    responsibilities: list[str]
    problems: list[str]
    problemDifficulty: ProblemDifficulty
    interviewTopics: list[str]


def extractJD(jd: str, retry: int = 1):
    for i in range(retry):
        response = model.generate_content(
            jd.strip(),
            generation_config=GenerationConfig(
                temperature=(i + 1) * 0.4,
                response_mime_type="application/json",
                response_schema=JobExtractedOutput,
            ),
        )
        try:
            print(response.text)
            return JobExtractedOutput(**json.loads(response.text))
        except Exception as e:
            print(e)
            pass
    return None
