from enum import Enum
from pydantic import BaseModel
from google.generativeai import GenerativeModel, GenerationConfig
import json

SYSTEM_INSTRUCTION = """
You are a senior developer. You will assist a friend finding job."""

model = GenerativeModel("gemini-1.5-flash-002", system_instruction=SYSTEM_INSTRUCTION)


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


class JobExtractedOutput(BaseModel):
    companyName: str | None
    jobTitle: str
    jobLevel: JobLevel
    yoe: int
    programmingLanguages: list[str]
    frameworks: list[str]
    skills: list[str]
    responsibilities: list[str]
    problems: list[ProblemTag]
    problemDifficulty: ProblemDifficulty
    interviewTopics: list[str]


def extractJD(jd: str, retry: int = 1):
    for i in range(retry):
        response = model.generate_content(
            jd.strip(),
            generation_config=GenerationConfig(
                temperature=i * 0.2,
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
